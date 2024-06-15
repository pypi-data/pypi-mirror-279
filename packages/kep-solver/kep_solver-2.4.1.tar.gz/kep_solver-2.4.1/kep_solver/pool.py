"""Handling of KEP pools, which are just the rules, procedures and
algorithms for a particular KEP.
"""

from time import thread_time
from typing import Optional

from kep_solver.entities import Instance
from kep_solver.model import Objective, Model, CycleAndChainModel, PICEF
from kep_solver.graph import Exchange


class ModelledExchange:
    """An exchange as modelled, including its value for various
    objectives and any other relevant information.
    """

    def __init__(self, exchange: Exchange, values: list[float]):
        """Constructor for ModelledExchange. Contains the Exchange object, and
        also the value of this exchange for the various objectives in this
        model.

        :param exchange: The exchange
        :param values: The value of this exchange for each objective
        """
        self._exchange = exchange
        self._values = values

    @property
    def exchange(self) -> Exchange:
        """The underlying exchange."""
        return self._exchange

    @property
    def values(self) -> list[float]:
        """The values of this exchange."""
        return self._values

    def __str__(self) -> str:
        """A human-readable representation of this exchange."""
        return str(self._exchange)


class Solution:
    """A solution to one instance of a KEP. Contains the exchanges, and
    the set of objective values attained.
    """

    def __init__(
        self,
        exchanges: list[ModelledExchange],
        scores: list[float],
        possible: list[ModelledExchange],
        times: list[tuple[str, float]],
        numSolutions: list[int],
    ):
        """Constructor for Solution. This class essentially just stores
        any information that may be useful.

        :param exchanges: the list of selected exchanges
        :param scores: the list of scores achieved for each objective
        :param possible: the set of possible exchanges, and their
            values for each objective
        :param times: The time taken for various operations. Each is a
            tuple with a string description of the action, and the time
            (in seconds)
        :param numSolutions: Either an empty list (if solutions weren't
            counted) or a list such that the i'th entry in the list is the
            number of distinct solutions found for the i'th objective
        """
        self._selected: list[ModelledExchange] = exchanges
        self._values: list[float] = scores
        self._possible: list[ModelledExchange] = possible
        self._times: list[tuple[str, float]] = times
        self._numSolutions = numSolutions

    @property
    def times(self) -> list[tuple[str, float]]:
        """Get the time taken for various operations. Each element of
        the returned list is a tuple where the first item is a string
        description of some operation, and the second item is the time
        taken in seconds.

        :return: the list of times (and their descriptions)
        """
        return self._times

    @property
    def selected(self) -> list[ModelledExchange]:
        """Get the selected solution.

        :return: the list of exchanges selected.
        """
        return self._selected

    @property
    def values(self) -> list[float]:
        """Get the Objective values of the selected solution.

        :return: the list of objective values
        """
        return self._values

    @property
    def possible(self) -> list[ModelledExchange]:
        """Return a list of all the possible chains and cycles that may
        be selected as ModelledExchange objects that contain the value of said
        exchange for each objective.

        :return: a list of cycles/chains as ModelledExchange objects
        """
        return self._possible

    @property
    def numSolutions(self) -> list[int]:
        """Return the number of optimal solutions found for each objective.

        :return: a list of cycles/chains as ModelledExchange objects
        """
        if not self._numSolutions:
            raise Exception("Error: Number of solutions was not calculated.")
        return self._numSolutions


class Pool:
    """A KEP pool."""

    def __init__(
        self,
        objectives: list[Objective],
        maxCycleLength: int,
        maxChainLength: int,
        description: str,
        build_alt_embed: int = 0,
        full_details: bool = True,
        model: type[Model] = CycleAndChainModel,
    ):
        """Constructor for Pool. This represents a set of objectives, and
        parameters for running matchings (such as maximum cycle and chain
        lengths).

        :param objectives: the list of objectives
        :param maxCycleLength: The longest cycle length allowed.
        :param maxChainLength: The longest chain length allowed. Note that the
            length of a chain includes the non-directed donor.
        :param description: A description of this pool.
        :param build_alt_embed: Whether to build alternate and embedded
            exchanges. build_alt_embed can be set to any of the following:

            0. Don't build alternate and embedded cycles. Faster, if you don't need alternate and embedded cycles
            1. Build all alternate and embedded cycles.
            2. Build only those alternate and embedded cycles that NHSBT expects
            3. Build only those alternate and embedded cycles that NHSBT expects, where embedded exchanges cannot use new donors
        :param full_details: If True, try to return details for all possible
            exchanges (even the ones not selected). Note that this will fail on
            some models that don't enumerate all possible exchnages.
        """
        # Create a copy of the list of objectives with the magic colon
        self._objectives: list[Objective] = objectives[:]
        self._maxCycleLength: int = maxCycleLength
        self._maxChainLength: int = maxChainLength
        self._full_details: bool = full_details
        self._description: str = description
        self._build_alt_embed = build_alt_embed
        self._modelClass = model

    @property
    def description(self) -> str:
        """A description of this pool."""
        return self._description

    @description.setter
    def description(self, desc) -> None:
        """A description of this pool."""
        self._description = desc

    @property
    def objectives(self) -> list[Objective]:
        """The list of objectives for this Pool."""
        return self._objectives

    @property
    def maxCycleLength(self) -> int:
        """The maximum length of cycles in this pool."""
        return self._maxCycleLength

    @property
    def maxChainLength(self) -> int:
        """The maximum length of chains in this pool. Note that this includes
        the non-directed donor, so a chain of length 1 only has a non-directed
        donor and no recipients."""
        return self._maxCycleLength

    def solve_single(
        self,
        instance: Instance,
        *,
        maxCycleLength: Optional[int] = None,
        maxChainLength: Optional[int] = None,
        countSolutions: bool = False,
        maxCount: Optional[list[int]] = None,
        solver=None,
    ) -> tuple[Optional[Solution], Model]:
        """Run a single instance through this pool, returning the solution, or
        None if no solution is found (e.g., if the solver crashes).

        :param instance: The instance to solve
        :param maxCycleLength: The longest cycle allowed. If not specified, we
            use the default from the Pool
        :param maxChainLength: The longest chain allowed. If not specified, we
            use the default from the Pool
        :param solver: An instantiated PuLP solver. If empty, a CBC solver is
            created and used
        :return: A tuple containing a Solution object, or None if an error
            occured, as well as the model that was solved.
        """
        if maxCycleLength is None:
            maxCycleLength = self._maxCycleLength
        if maxChainLength is None:
            maxChainLength = self._maxChainLength
        t = thread_time()
        model = self._modelClass(
            instance,
            self._objectives,
            maxChainLength=maxChainLength,
            maxCycleLength=maxCycleLength,
            build_alt_embed=self._build_alt_embed,
        )
        times = [("Model building", thread_time() - t)]
        t = thread_time()
        solution, model_times, numSolutions = model.solve(
            countSolutions, maxCount, solver
        )
        times.extend(model_times)
        times.append(("Total model solving", thread_time() - t))
        if solution is None:
            return None
        values = model.objective_values
        if self._full_details:
            exchange_values: dict[Exchange, list[float]] = {
                exchange: model.exchange_values(exchange)
                for exchange in model.exchanges
            }
            solutions = [ModelledExchange(ex, exchange_values[ex]) for ex in solution]
            possible = [
                ModelledExchange(ex, exchange_values[ex])
                for ex in exchange_values.keys()
            ]
            return Solution(solutions, values, possible, times, numSolutions), model
        else:
            solutions = [
                ModelledExchange(ex, model.exchange_values(ex)) for ex in solution
            ]
            return Solution(solutions, values, [], times, numSolutions), model

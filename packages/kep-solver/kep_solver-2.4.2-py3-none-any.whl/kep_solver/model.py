from collections import defaultdict
from collections.abc import ValuesView
from enum import Enum
from time import thread_time
from typing import Optional, Union

import pulp  # type: ignore
import warnings  # We use this to ignore one specific warning from pulp


from kep_solver.entities import Instance, Donor
from kep_solver.graph import (
    CompatibilityGraph,
    Vertex,
    Edge,
    Exchange,
    build_alternates_and_embeds,
)


class Sense(Enum):
    """An enumeration of the sense of an objective."""

    MAX = 1
    MIN = 2
    EXACT = 3

    def toConstraint(self):
        """Converts a Sense into a constraint type suitable for use
        with PuLP

        :return: constraint sense
        """
        if self.name == "MAX":
            return pulp.LpConstraintGE
        elif self.name == "MIN":
            return pulp.LpConstraintLE
        else:
            return pulp.LpConstraintEQ

    def toObjective(self):
        """Converts a Sense into an objective type suitable for use
        with PuLP

        :return: objective sense
        """
        if self.name == "MAX":
            return pulp.LpMaximize
        elif self.name == "MIN":
            return pulp.LpMinimize
        else:
            raise Exception("Exact objective doesn't make sense")


class Objective:
    """A base class for an objective."""

    def __init__(self):
        raise Exception("Plain Objective objects cannot be instantiated")

    def edgeValue(
        self, graph: CompatibilityGraph, edge: Edge, position: Optional[int] = None
    ) -> float:
        """What value should the given transplant in the given graph be given,
        if it is at the given position (i.e., position = 1 means this is the
        first edge in a chain)?

        :param graph: The graph containing the exchange
        :param edge: The edge, representing a transplant
        :param position: The position of this edge in an exchange
        :return: The value of this edge in this position
        """
        raise Exception("Edge value not defined for this objective")

    def value(self, graph: CompatibilityGraph, exchange: Exchange) -> float:
        """What value should the given exchange in the given graph
        be given?

        :param graph: The graph containing the exchange
        :param exchange: A cycle or chain.
        """
        return sum(
            self.edgeValue(graph, edge) for edge in graph.exchangeEdges(exchange)
        )

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        raise Exception("Plain Objective objects should not be instantiated or called")

    @property
    def sense(self) -> Sense:
        """The sense of the objective."""
        raise Exception("Plain Objective objects should not be instantiated or called")


class TransplantCount(Objective):
    """An objective to maximise the number of transplants. Note that
    for a chain, the donation to the non-directed donor (which often
    would go to a deceased-donor waiting list) is counted as a
    transplant.
    """

    def __init__(self):
        pass

    def edgeValue(
        self, graph: CompatibilityGraph, edge: Edge, position: Optional[int] = None
    ) -> float:
        """What value should the given transplant in the given graph be given,
        if it is at the given position (i.e., position = 1 means this is the
        first edge in a chain)?

        :param graph: The graph containing the exchange
        :param edge: The edge, representing a transplant
        :param position: The position of this edge in an exchange
        :return: The value of this edge in this position
        """
        return 1

    def value(self, graph: CompatibilityGraph, exchange: Exchange) -> float:
        """How many transplants does the given exchange represent.

        :param graph: The graph containing the exchange
        :param exchange: A cycle or chain.
        :return: the number of transplants
        """
        return len(exchange)

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Number of transplants"

    @property
    def sense(self) -> Sense:
        """This is a maximisation objective."""
        return Sense.MAX


class EffectiveTwoWay(Objective):
    """An objective to maximise the number of effective two-way
    transplants.  For cycles, they must either have size two, or have
    a back-arc. All chains count as effective two-way exchanges. This
    is binary for each exchange.  That is, either an exchange has or
    does not have an effective two-way exchange.
    """

    def __init__(self):
        pass

    def value(self, graph: CompatibilityGraph, exchange: Exchange) -> float:
        """Does the given exchange contain an effective two-way
        exchange?

        :param graph: The graph containing the exchange
        :param exchange: A cycle or chain.
        :return: 1 if and only if it is effectively two-way
        """
        if len(exchange) == 2:
            return 1
        if len(exchange) == 3 and (
            exchange.num_backarcs_uk() >= 1 or exchange[0].isNdd()
        ):
            return 1
        return 0

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Number of effective two-way exchanges"

    @property
    def sense(self) -> Sense:
        """This is a maximisation objective."""
        return Sense.MAX


class BackArcs(Objective):
    """An objective to maximise the number of back-arcs. Note that
    arcs back to a non-directed donor are not considered backarcs in
    this objective.
    """

    def __init__(self):
        pass

    def value(self, graph: CompatibilityGraph, exchange: Exchange) -> float:
        """How many backarcs does the given exchange contain?

        :param graph: The graph containing the exchange
        :param exchange: An exchange
        :return: The number of backarcs in the exchange
        """
        if len(exchange) == 3:
            return exchange.num_backarcs_uk()
        return 0

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Number of backarcs"

    @property
    def sense(self) -> Sense:
        """This is a maximisation objective."""
        return Sense.MAX


def UK_age_score(d1: Donor, d2: Donor) -> tuple[float, float]:
    """Calculate and return the age difference bonus and tiebreaker value for a
    given transplant where d1 is a Donor donating to the paired recipient of
    Donor d2. The age difference bonus is 3, if the ages of the two donors
    differ by at most 20, and the tie breaker is given by the equation

      (70 - age_difference)^2 * 1e-5

    Note that as a recipient may have multiple donors, this value is dependant
    not only on a Transplant in an Exchange, but also which Transplant will
    occur next. If d1 is a non-directed Donor, both the age difference bonus
    and the tiebreaker will be 0.

    :param d1: The Donor donating to the paired recipient of d2
    :param d2: A paired donor of d1
    :return: A tuple containing the age difference bonus, and the tiebreaker value.
    """
    _age_weight_selector = 20
    _age_weight = 3
    _age_diff_factor = 1e-5
    _max_age_diff = 70

    if d2.NDD:
        return 0, 0
    age_diff = abs(d1.age - d2.age)
    tb = _age_diff_factor * ((_max_age_diff - age_diff) ** 2)
    tb = round(tb, 5)
    if age_diff <= _age_weight_selector:
        return _age_weight, tb
    return 0, tb


class UKScore(Objective):
    """An objective to maximise the number of back-arcs."""

    def __init__(self):
        pass

    def value(self, graph: CompatibilityGraph, exchange: Exchange) -> float:
        """What is the UK score of this exchange?

        :param graph: The graph containing the exchange
        :param exchange: An exchange
        :return: The UK score of this exchange
        """
        score: float = 0.0
        for ind, source in enumerate(exchange):
            target_v = exchange[(ind + 1) % len(exchange)]
            donor = source.donor
            if not target_v.donor.NDD:
                recipient = target_v.donor.recipient
                transplants = [
                    t for t in donor.transplants() if t.recipient == recipient
                ]
                assert len(transplants) == 1
                transplant = transplants[0]
                score += transplant.weight
                bonus, tb = UK_age_score(donor, target_v.donor)
                score += bonus + tb
        return round(score, 5)

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Total score (UK calculation)"

    @property
    def sense(self) -> Sense:
        """This is a maximisation objective."""
        return Sense.MAX


class ThreeWay(Objective):
    """An objective to minimise the number of three-way exchanges. If
    no larger exchanges are allowed, this has the effect of increasing
    the number of two-way exchanges.
    """

    def __init__(self):
        pass

    def value(self, graph: CompatibilityGraph, exchange: Exchange) -> float:
        """Is the given exchange a three-way exchange.

        :param graph: The graph containing the exchange
        :param exchange: A cycle or chain.
        :return: 1 if and only if it is a three-way exchange
        """
        if len(exchange) == 3:
            return 1
        return 0

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Number of three-way exchanges"

    @property
    def sense(self) -> Sense:
        """This is a minimisation objective."""
        return Sense.MIN


class Model(pulp.LpProblem):
    """A base class for all models for KEPs. Any new models should
    inherit from this and implement all associated functions.
    """

    supports: list[type[Objective]] = []

    def __init__(
        self,
        instance: Instance,
        objectives: list[Objective],
        *,
        maxCycleLength: int,
        maxChainLength: int,
        build_alt_embed: int = 0,
    ):
        """Create a Model. Note that this base class has no implementation and
        should not be directly constructed.

        :param instance: The instance to build the model from
        :param objectives: The list of objectives for this pool
        :param maxCycleLength: The maximum length of a cycle
        :param maxChainLength: The maximum length of a chain
        :param build_alt_embed: Whether to build alternate and embedded
            exchanges. build_alt_embed can be set to any of the following:

            0. Don't build alternate and embedded cycles. Faster, if you don't need alternate and embedded cycles
            1. Build all alternate and embedded cycles.
            2. Build only those alternate and embedded cycles that NHSBT expects
            3. Build only those alternate and embedded cycles that NHSBT expects, where embedded exchanges cannot use new donors
        """
        super().__init__()
        self._instance: Instance = instance
        self._graph: CompatibilityGraph = CompatibilityGraph(instance)
        # List comprehension to make a copy of the list of objectives
        self._objectives: list[Objective] = [obj for obj in objectives]
        self._objective_values: list[float] = []
        self._maxCycleLength = maxCycleLength
        self._maxChainLength = maxChainLength
        self._build_alt_embed = build_alt_embed

    @property
    def cycles(self) -> ValuesView[Exchange]:
        """Return the list of cycles in this model.

        :return: the list of cycles
        """
        raise Exception("Not implemented")

    @property
    def chains(self) -> ValuesView[Exchange]:
        """Return the list of chains in this model.

        :return: the list of chains
        """
        raise Exception("Not implemented")

    @property
    def exchanges(self) -> list[Exchange]:
        """Return the list of cycles and chains in this model.

        :return: the list of cycles and chains
        """
        raise Exception("Not implemented")

    def exchange_values(self, exchange: Exchange) -> list[float]:
        """Given an exchange, return the value of the exchange for
        each objective.

        :param exchange: The exchange whose value is to be returned
        :return: the list of values of this exchange
        """
        raise Exception("Not implemented")

    def support(self, objective: Objective) -> bool:
        """Can this model solve for the given objective.

        :param objective: The objective to solve
        :return: Can this model solve the given objective
        """
        return bool([isinstance(objective, supported) for supported in self.supports])

    def addObjectiveConstraint(self, objective: Objective, value: float, index: int):
        """Add a constraint that ensures the previous objective keeps
        its value.

        :param objective: The previous objective
        :param value: The value the previous objective attained
        :param index: Which number objective is this (only used for
            naming the constraint)
        """
        raise Exception("Plain Model objects should not be instantiated or called")

    def solve(
        self,
        countSolutions: bool = False,
        maxCount: Optional[list[int]] = None,
        solver=None,
    ) -> tuple[list[Exchange], list[tuple[str, float]], list[int]]:
        """Solve the model to find an optimal solution.

        :param countSolutions: If true, count the number of distinct solutions
            found at each level of optimisation. Note that this solves a new
            optimisation problem for each such solution found, and thus can be very
            time-consuming.

        :param solver: An instantiated PuLP solver. If empty, a solver will be
            created and used

        :return: A list of selected transplants, a list of the time taken
            to solve for each objective in the pool, and a list of the number
            of optimal solutions found for each objective
        """
        raise Exception("Plain Model objects should not be instantiated or called")


class PICEF(Model):
    """A model that represents each cycle by a variable, but otherwise
    represents edges in chains as a variable.
    """

    supports = [TransplantCount]

    def __init__(
        self,
        instance: Instance,
        objectives: list[Objective],
        *,
        maxCycleLength: int,
        maxChainLength: int,
        build_alt_embed: int = 0,
    ):
        """Construct a PICEF model from an instance.

        :param instance: The instance to build the model from
        :param objectives: The list of objectives for this pool
        :param maxCycleLength: The maximum length of a cycle
        :param maxChainLength: The maximum length of a chain
        :param build_alt_embed: Determines which alternative and embedded
            exchanges should be enumerated. For PICEF, this must be set to zero.
        """
        if build_alt_embed != 0:
            raise Exception(f"Unable to use PICEF with {build_alt_embed=}")
        super().__init__(
            instance,
            objectives,
            maxCycleLength=maxCycleLength,
            maxChainLength=maxChainLength,
            build_alt_embed=0,
        )
        self._cycles: dict[pulp.LpVariable, Exchange] = {}
        self._vars_by_vertex: dict[Vertex, list[pulp.LpVariable]] = {}
        self._vars_by_exchange: dict[Exchange, pulp.LpVariable] = {}
        self._chain_edge_vars: dict[Edge, list[pulp.LpVariable]] = defaultdict(list)
        self._chain_vars_out: dict[int, dict[int, list[pulp.LpVariable]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self._chain_vars_in: dict[int, dict[int, list[pulp.LpVariable]]] = defaultdict(
            lambda: defaultdict(list)
        )

    @property
    def cycles(self) -> ValuesView[Exchange]:
        """Return the list of cycles in this model.

        :return: the list of cycles
        """
        return self._cycles.values()

    @property
    def chains(self) -> ValuesView[Exchange]:
        """Return the list of chains in this model.

        :return: the list of chains
        """
        raise Exception("chains() not implemented for PICEF")

    @property
    def exchanges(self) -> list[Exchange]:
        """Return the list of cycles and chains in this model.

        :return: the list of cycles and chains
        """
        raise Exception("It's vague to do this now as what is chains()? in PICEF")
        return list(self.chains) + list(self.cycles)

    @property
    def graph(self) -> CompatibilityGraph:
        """The graph used for this model.

        :return: The graph used for this model.
        """
        return self._graph

    def exchange_values(self, exchange: Exchange) -> list[float]:
        """Given an exchange, return the value of the exchange for
        each objective.

        :param exchange: The exchange whose value is to be returned
        :return: the list of values of this exchange
        """
        return [
            objective.value(self._graph, exchange) for objective in self._objectives
        ]

    def _var_from_donor(self, donor: Donor) -> pulp.LpVariable:
        """Given a donor, find its corresponding variable. This means
        going via the CompatibilityGraph.

        :param donor: the donor to search for
        :return: the donor's variable
        """
        return self._vars_by_vertex[self._graph.donorVertex(donor)]

    def _var_from_exchange(self, exchange: Exchange) -> pulp.LpVariable:
        """Given an exchange, get the variable representing it.

        :param exchange: the exchange to search for
        :return: the exchange's variable
        """
        return self._vars_by_exchange[exchange]

    def _build_chain_vars(self) -> None:
        """Build the variables for chain variables."""
        if self._maxChainLength == 0:
            return
        donor_queue: list[tuple[Donor, int]] = [
            (d, 1) for d in self._instance.activeDonors() if d.NDD
        ]
        done: set[tuple[int, Union[str, int], int]] = set()
        while donor_queue:
            donor, length = donor_queue.pop(0)
            vertex = self._graph.donorVertex(donor)
            if length < self._maxChainLength:
                for e in vertex.edgesOut:
                    tup = (vertex.index, e.end.index, length)
                    if tup in done:
                        continue
                    var = pulp.LpVariable(
                        f"chain_{vertex.index}_{e.end.index}_{length}", cat="Binary"
                    )
                    var.position = length
                    done.add(tup)
                    self._chain_vars_out[vertex.index][length].append(var)
                    self._chain_vars_in[e.end.index][length].append(var)
                    self._chain_edge_vars[e].append(var)
                    donor_queue.append((e.end.donor, length + 1))
            var = pulp.LpVariable(f"chain_{vertex.index}_sink_{length}", cat="Binary")
            var.position = length
            stup = (vertex.index, "sink", length)
            if stup in done:
                continue
            done.add(stup)
            self._chain_vars_out[vertex.index][length].append(var)
            sink = Edge(donor, vertex, Vertex.sink())
            self._chain_edge_vars[sink].append(var)

        return

    def _build_chain_constraints(self) -> None:
        """Build the constraints for chain variables."""
        for v in self._graph.vertices:
            if v.index not in self._chain_vars_out:
                continue
            if v.isNdd():
                length = 1
                # At most one donation from an NDD
                name = f"vertex_ndd_{str(v)}_{length}_max"
                self += (
                    pulp.lpSum(self._chain_vars_out[v.index][length]) <= 1,
                    name,
                )
            else:
                for length in range(2, self._maxChainLength + 1):
                    # Don't donate unless you get a donation
                    name = f"vertex_{str(v)}_{length}_flow"
                    self += (
                        pulp.lpSum(self._chain_vars_out[v.index][length])
                        <= pulp.lpSum(self._chain_vars_in[v.index][length - 1]),
                        name,
                    )

    def _build_chains_from_edges(self, selected: list[Edge]) -> list[Exchange]:
        """Given a set of edges in a graph (specifically, the compatibility
        graph associated with this model), build the associated set of chains.

        :param: selected The selected edges to be used
        :return: The list of chains corresponding to these edges
        """

        def build_chain(verts_so_far):
            for e in verts_so_far[-1].edgesOut:
                if e in selected:
                    verts_so_far.append(e.end)
                    build_chain(verts_so_far)

        chains: list[Exchange] = []
        for donor in self._instance.activeDonors():
            if not donor.NDD:
                continue
            chain_verts = [self._graph.donorVertex(donor)]
            build_chain(chain_verts)
            chains.append(Exchange(f"{len(chains)}", chain_verts))
        return chains

    def build_model(self) -> None:
        """Build the model. That is, create all the variables and
        constraints."""
        for vertex in self._graph.vertices:
            self._vars_by_vertex[vertex] = []
        for cycle in self._graph.findCycles(self._maxCycleLength):
            var = pulp.LpVariable(f"cycle_{len(self._cycles)}", cat="Binary")
            for vertex in cycle.vertices:
                self._vars_by_vertex[vertex].append(var)
            self._vars_by_exchange[cycle] = var
            self._cycles[var] = cycle
        self._build_chain_vars()
        self._build_chain_constraints()
        for recipient in self._instance.activeRecipients():
            name = f"recipient_{str(recipient)}"
            self += (
                pulp.lpSum(self._var_from_donor(donor) for donor in recipient.donors())
                + pulp.lpSum(
                    pulp.lpSum(
                        pulp.lpSum(
                            self._chain_vars_in[self._graph.donorVertex(donor).index][
                                length
                            ]
                        )
                        for length in range(1, self._maxChainLength + 1)
                    )
                    for donor in recipient.donors()
                )
                <= 1,
                name,
            )

    def addObjectiveConstraint(self, objective: Objective, value: float, index: int):
        """Adds a constraint that ensures the previous objective keeps
        its value.

        :param objective: The previous objective
        :param value: The value the previous objective attained
        :param index: Which number objective is this (only used for
            naming the constraint)
        """
        equation = pulp.lpSum(
            objective.value(self._graph, cycle) * var
            for var, cycle in self._cycles.items()
        )
        equation += pulp.lpSum(
            objective.edgeValue(self._graph, edge, var.position) * var
            for edge, edge_vars in self._chain_edge_vars.items()
            for var in edge_vars
        )
        con = pulp.LpConstraint(
            equation,
            sense=objective.sense.toConstraint(),
            rhs=value,
            name=f"ObjCon_{index}",
        )
        self += con

    def countSolutions(self, maxCount: Optional[int] = None) -> int:
        """Count the number of distinct solutions available for this instance at this objective.

        Note that this can drastically increase the running time (by several
        orders of magnitude) as for each distinct solution we need to solve a
        new IP model.
        """
        raise Exception("Not yet implemented")
        solver = pulp.getSolver("PULP_CBC_CMD", msg=False)
        copy = self.copy()
        pulp.LpProblem.solve(copy, solver)
        solns = 1
        target = pulp.valueOrDefault(copy.objective)
        while True:
            selected = [x for x in copy.variables() if x.value() > 0.9]
            copy += pulp.LpConstraint(
                pulp.lpSum(selected),
                sense=pulp.LpConstraintLE,
                rhs=len(selected) - 1,  # -1 for less-or-equal
                name=f"Avoid_soln_{solns}",
            )
            pulp.LpProblem.solve(copy, solver)
            objective = pulp.valueOrDefault(copy.objective)
            if (
                copy.status != pulp.constants.LpStatusOptimal
                or abs(target - objective) > 1e-4
            ):
                return solns
            solns += 1
            if maxCount and solns >= maxCount:
                return solns

    def solve(
        self,
        countSolutions: bool = False,
        maxCount: Optional[list[int]] = None,
        solver=None,
    ) -> tuple[list[Exchange], list[tuple[str, float]], list[int]]:
        """Solve the model to find an optimal solution.

        :param countSolutions: If true, count the number of distinct solutions
            found at each level of optimisation. Note that this solves a new
            optimisation problem for each such solution found, and thus can be very
            time-consuming.

        :param solver: An instantiated PuLP solver. If empty, a CBC solver is
            created and used

        :return: A list of selected transplants, a list of the time taken
            to solve for each objective in the pool, and a list of the number
            of optimal solutions found for each objective
        """
        self.build_model()
        selected: list[Exchange] = []
        num_solutions: list[int] = []
        times: list[tuple[str, float]] = []
        if solver is None:
            solver = pulp.getSolver("PULP_CBC_CMD", msg=False)
        for index, obj in enumerate(self._objectives):
            obj_equation = pulp.lpSum(
                obj.value(self._graph, cycle) * var
                for var, cycle in self._cycles.items()
            )
            obj_equation += pulp.lpSum(
                obj.edgeValue(self._graph, edge, var.position) * var
                for edge, edge_vars in self._chain_edge_vars.items()
                for var in edge_vars
            )
            # If there is nothing in the objective function, we skip it.
            # Otherwise, PuLP sometimes has issues.
            if not obj_equation:
                self._objective_values.append(0)
                continue
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore", "Overwriting previously set objective."
                )
                self += obj_equation
            self.sense = obj.sense.toObjective()
            t = thread_time()
            pulp.LpProblem.solve(self, solver)
            if self.status != pulp.constants.LpStatusOptimal:
                raise Exception("Optimising returned non-optimal, no solution found")
            self._objective_values.append(pulp.valueOrDefault(self.objective))
            if countSolutions:
                limit = None
                if maxCount:
                    limit = maxCount[index]
                num_solutions.append(self.countSolutions(limit))
            times.append((f"Solving {obj.describe()}", thread_time() - t))
            if index < len(self._objectives) - 1:
                self.addObjectiveConstraint(obj, self._objective_values[-1], index)
            else:
                for var, cycle in self._cycles.items():
                    if var.value() > 0.9:
                        selected.append(cycle)
                selected_edges: list[Edge] = []
                for edge, varList in self._chain_edge_vars.items():
                    if any(var.value() > 0.9 for var in varList):
                        selected_edges.append(edge)
                selected.extend(self._build_chains_from_edges(selected_edges))
        return selected, times, num_solutions

    @property
    def objective_values(self) -> list[float]:
        """The list of all objective values."""
        return self._objective_values

    def objective_value(self, objective_index: int) -> float:
        """Return the value of an objective, if it has been solved.
        If this model has not been solved, accessing this raises an
        error.

        :param objective_index: the index of the objective whose value
            is to be returned
        :return: the value of the objective as given by objective_index
        """
        if not self._objective_values:
            raise Exception("Tried to get objective value when model is not solved.")
        return self._objective_values[objective_index]


class CycleAndChainModel(Model):
    """A model that represents each cycle or chain with a binary
    variable.  Note that since CompatibilityGraph has one vertex per
    donor, and recipients may have multiple donors, this means that
    constraints may be needed to ensure at most one donor per recipient
    is selected.

    """

    supports = [TransplantCount]

    def __init__(
        self,
        instance: Instance,
        objectives: list[Objective],
        *,
        maxCycleLength: int,
        maxChainLength: int,
        build_alt_embed: int = 0,
    ):
        """Construct a CycleAndChainModel from an instance.

        :param instance: The instance to build the model from
        :param objectives: The list of objectives for this pool
        :param maxCycleLength: The maximum length of a cycle
        :param maxChainLength: The maximum length of a chain
        :param build_alt_embed: Whether to build alternate and embedded
            exchanges. build_alt_embed can be set to any of the following:

            0. Don't build alternate and embedded cycles. Faster, if you don't need alternate and embedded cycles
            1. Build all alternate and embedded cycles.
            2. Build only those alternate and embedded cycles that NHSBT expects
            3. Build only those alternate and embedded cycles that NHSBT expects, where embedded exchanges cannot use new donors
        """
        super().__init__(
            instance,
            objectives,
            maxCycleLength=maxCycleLength,
            maxChainLength=maxChainLength,
            build_alt_embed=build_alt_embed,
        )
        self._cycles: dict[pulp.LpVariable, Exchange] = {}
        self._chains: dict[pulp.LpVariable, Exchange] = {}
        self._vars_by_vertex: dict[Vertex, list[pulp.LpVariable]] = {}
        self._vars_by_exchange: dict[Exchange, pulp.LpVariable] = {}

    @property
    def cycles(self) -> ValuesView[Exchange]:
        """Return the list of cycles in this model.

        :return: the list of cycles
        """
        return self._cycles.values()

    @property
    def chains(self) -> ValuesView[Exchange]:
        """Return the list of chains in this model.

        :return: the list of chains
        """
        return self._chains.values()

    @property
    def exchanges(self) -> list[Exchange]:
        """Return the list of cycles and chains in this model.

        :return: the list of cycles and chains
        """
        return list(self.chains) + list(self.cycles)

    def exchange_values(self, exchange: Exchange) -> list[float]:
        """Given an exchange, return the value of the exchange for
        each objective.

        :param exchange: The exchange whose value is to be returned
        :return: the list of values of this exchange
        """
        return [
            objective.value(self._graph, exchange) for objective in self._objectives
        ]

    def _var_from_donor(self, donor: Donor) -> pulp.LpVariable:
        """Given a donor, find its corresponding variable. This means
        going via the CompatibilityGraph.

        :param donor: the donor to search for
        :return: the donor's variable
        """
        return self._vars_by_vertex[self._graph.donorVertex(donor)]

    def _var_from_exchange(self, exchange: Exchange) -> pulp.LpVariable:
        """Given an exchange, get the variable representing it.

        :param exchange: the exchange to search for
        :return: the exchange's variable
        """
        return self._vars_by_exchange[exchange]

    def build_model(self) -> None:
        """Build the model. That is, create all the variables and
        constraints."""
        # Track the chains each NDD can be in
        chains_by_ndd: dict[Donor, list[pulp.LpVariable]] = {}
        for nondirected in self._instance.activeDonors():
            if not nondirected.NDD:
                continue
            chains_by_ndd[nondirected] = []
        for vertex in self._graph.vertices:
            self._vars_by_vertex[vertex] = []
        for cycle in self._graph.findCycles(self._maxCycleLength):
            var = pulp.LpVariable(f"cycle_{len(self._cycles)}", cat="Binary")
            for vertex in cycle.vertices:
                self._vars_by_vertex[vertex].append(var)
            self._vars_by_exchange[cycle] = var
            self._cycles[var] = cycle
        # This particular model expects cycles and chains to have different ID
        # numbers, hence the index_offset.
        for chain in self._graph.findChains(
            self._maxChainLength, index_offset=len(self.cycles)
        ):
            var = pulp.LpVariable(f"chain_{len(self._chains)}", cat="Binary")
            for vertex in chain:
                self._vars_by_vertex[vertex].append(var)
            self._chains[var] = chain
            chains_by_ndd[chain[0].donor].append(var)
            self._vars_by_exchange[chain] = var

        # Note that self._build_alt_embed - 1 must map onto the uk_variant
        # parameter of the build_alternates_and_embeds function
        build_alternates_and_embeds(
            list(self._cycles.values()) + list(self._chains.values()),
            uk_variant=self._build_alt_embed - 1,
        )
        for recipient in self._instance.activeRecipients():
            name = f"recipient_{str(recipient)}"
            self += (
                pulp.lpSum(self._var_from_donor(donor) for donor in recipient.donors())
                <= 1,
                name,
            )
        # Add constraint that each NDD can be used at most once.
        for nondirected in self._instance.activeDonors():
            if not nondirected.NDD:
                continue
            name = f"ndd_{str(nondirected)}"
            self += pulp.lpSum(chains_by_ndd[nondirected]) <= 1, name

    def addObjectiveConstraint(self, objective: Objective, value: float, index: int):
        """Adds a constraint that ensures the previous objective keeps
        its value.

        :param objective: The previous objective
        :param value: The value the previous objective attained
        :param index: Which number objective is this (only used for
            naming the constraint)
        """
        equation = pulp.lpSum(
            objective.value(self._graph, cycle) * var
            for var, cycle in self._cycles.items()
        )
        equation += pulp.lpSum(
            objective.value(self._graph, chain) * var
            for var, chain in self._chains.items()
        )
        con = pulp.LpConstraint(
            equation,
            sense=objective.sense.toConstraint(),
            rhs=value,
            name=f"ObjCon_{index}",
        )
        self += con

    def countSolutions(self, maxCount: Optional[int] = None) -> int:
        """Count the number of distinct solutions available for this instance at this objective.

        Note that this can drastically increase the running time (by several
        orders of magnitude) as for each distinct solution we need to solve a
        new IP model.
        """
        solver = pulp.getSolver("PULP_CBC_CMD", msg=False)
        copy = self.copy()
        pulp.LpProblem.solve(copy, solver)
        solns = 1
        target = pulp.valueOrDefault(copy.objective)
        while True:
            selected = [x for x in copy.variables() if x.value() > 0.9]
            copy += pulp.LpConstraint(
                pulp.lpSum(selected),
                sense=pulp.LpConstraintLE,
                rhs=len(selected) - 1,  # -1 for less-or-equal
                name=f"Avoid_soln_{solns}",
            )
            pulp.LpProblem.solve(copy, solver)
            objective = pulp.valueOrDefault(copy.objective)
            if (
                copy.status != pulp.constants.LpStatusOptimal
                or abs(target - objective) > 1e-4
            ):
                return solns
            solns += 1
            if maxCount and solns >= maxCount:
                return solns

    def solve(
        self,
        countSolutions: bool = False,
        maxCount: Optional[list[int]] = None,
        solver=None,
    ) -> tuple[list[Exchange], list[tuple[str, float]], list[int]]:
        """Solve the model to find an optimal solution.

        :param countSolutions: If true, count the number of distinct solutions
            found at each level of optimisation. Note that this solves a new
            optimisation problem for each such solution found, and thus can be very
            time-consuming.

        :param solver: An instantiated PuLP solver. If empty, a CBC solver is
            created and used

        :return: A list of selected transplants, a list of the time taken
            to solve for each objective in the pool, and a list of the number
            of optimal solutions found for each objective
        """
        self.build_model()
        selected: list[Exchange] = []
        num_solutions: list[int] = []
        times: list[tuple[str, float]] = []
        exchanges: list[Exchange] = list(self._cycles.values())
        exchanges += list(self._chains.values())
        if solver is None:
            solver = pulp.getSolver("PULP_CBC_CMD", msg=False)
        for index, obj in enumerate(self._objectives):
            obj_equation = pulp.lpSum(
                obj.value(self._graph, exchange) * self._var_from_exchange(exchange)
                for exchange in exchanges
            )
            # If there is nothing in the objective function, we skip it.
            # Otherwise, PuLP sometimes has issues.
            if not obj_equation:
                self._objective_values.append(0)
                continue
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore", "Overwriting previously set objective."
                )
                self += obj_equation
            self.sense = obj.sense.toObjective()
            t = thread_time()
            pulp.LpProblem.solve(self, solver)
            if self.status != pulp.constants.LpStatusOptimal:
                raise Exception("Optimising returned non-optimal, no solution found")
            self._objective_values.append(pulp.valueOrDefault(self.objective))
            if countSolutions:
                limit = None
                if maxCount:
                    limit = maxCount[index]
                num_solutions.append(self.countSolutions(limit))
            times.append((f"Solving {obj.describe()}", thread_time() - t))
            if index < len(self._objectives) - 1:
                self.addObjectiveConstraint(obj, self._objective_values[-1], index)
            else:
                for var, cycle in self._cycles.items():
                    if var.value() > 0.9:
                        selected.append(cycle)
                for var, chain in self._chains.items():
                    if var.value() > 0.9:
                        selected.append(chain)
        return selected, times, num_solutions

    @property
    def objective_values(self) -> list[float]:
        """The list of all objective values."""
        return self._objective_values

    def objective_value(self, objective_index: int) -> float:
        """Return the value of an objective, if it has been solved.
        If this model has not been solved, accessing this raises an
        error.

        :param objective_index: the index of the objective whose value
            is to be returned
        :return: the value of the objective as given by objective_index
        """
        if not self._objective_values:
            raise Exception("Tried to get objective value when model is not solved.")
        return self._objective_values[objective_index]

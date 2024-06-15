**************************
Frequently asked questions
**************************

How can I set a timeout when solving models?

  The :func:`kep_solver.model.Model.solve` and :func:`kep_solver.pool.Pool.solve_single` functions both support a parameter called `solver`, which is a PuLP solver object.
  Amongst other things, this solver can be configured with a timeout or time limit as follows:
  ::

        from pulp import apis
        time_limited_solver = apis.COIN_CMD(timeLimit=60)
        model.solve(solver=time_limited_solver)

  Note that PuLP supports `many other solvers <https://coin-or.github.io/pulp/technical/solvers.html>`_ that you can try, but some of them may not be available.

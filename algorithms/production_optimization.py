from typing import Any

from ortools.linear_solver.pywraplp import Solver


def solve_problem() -> None:
    solver: Solver = Solver("simple_mip_program", Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    x: Any = solver.IntVar(0, 100, "x")
    y: Any = solver.IntVar(0, 100, "y")

    solver.Add(1 * x + 2 * y <= 40)
    solver.Add(4 * x + 4 * y <= 80)
    solver.Add(3 * x + 1 * y <= 50)

    solver.Maximize(x * 5.0 + y * 4.0)

    status: Any = solver.Solve()

    if status == Solver.OPTIMAL or status == Solver.FEASIBLE:
        print("Solution: OK")
        print("Objective value =", solver.Objective().Value())

        if x.solution_value() > 0.5:
            print("x =", x.solution_value())
            print("y =", y.solution_value())
        print("Time = ", solver.WallTime(), " milliseconds")
    else:
        print("The problem does not have an optimal solution.")


if __name__ == "__main__":
    solve_problem()

from typing import Any, Dict, List

from ortools.linear_solver.pywraplp import Solver

VOLUMES: List = [3, 4, 6, 1, 5]
VALUES: List = [6, 7, 8, 1, 4]
CAPASITY: int = 12


def solve_problem() -> None:
    solver: Solver = Solver("simple_mip_program", Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    backet: Dict = {j: solver.BoolVar(f"x{j}") for j in range(5)}

    solver.Add(
        solver.Sum(list(VOLUMES[j] * backet[j] for j in range(len(VOLUMES))))
        <= CAPASITY
    )

    solver.Maximize(
        solver.Sum(list(VALUES[j] * backet[j] for j in range(len(VOLUMES))))
    )

    status: Any = solver.Solve()

    if status == Solver.OPTIMAL or status == Solver.FEASIBLE:
        print("Solution: OK")
        print("Objective value =", solver.Objective().Value())
        print("culculate Time = ", solver.WallTime(), " milliseconds")

        print("select item")
        for j in range(len(VOLUMES)):
            print(j, backet[j].solution_value())

        print("total value")
        print(sum(VALUES[j] * backet[j].solution_value() for j in range(len(VOLUMES))))

    else:
        print("The problem does not have an optimal solution.")


if __name__ == "__main__":
    solve_problem()

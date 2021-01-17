from typing import Any, Dict, List, Tuple

from ortools.linear_solver.pywraplp import Solver

COST: List = [
    [10, 10, 11, 17],
    [16, 19, 12, 14],
    [15, 12, 14, 12],
]


def solve_problem() -> None:
    solver: Solver = Solver("simple_mip_program", Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    amount: Dict = {}
    for i in range(3):
        for j in range(4):
            amount[i, j] = solver.IntVar(0, 50, f"val{i}_{j}")

    amount_w1, amount_w2, amount_w3 = get_quantity_carried_out(amount)
    solver.Add(amount_w1 <= 35)
    solver.Add(amount_w2 <= 41)
    solver.Add(amount_w3 <= 42)

    amount_f1, amount_f2, amount_f3, amount_f4 = get_quantity_carried_in(amount)
    solver.Add(amount_f1 >= 28)
    solver.Add(amount_f2 >= 29)
    solver.Add(amount_f3 >= 31)
    solver.Add(amount_f4 >= 25)

    solver.Minimize(
        solver.Sum([amount[i, j] * COST[i][j] for i in range(3) for j in range(4)])
    )

    status: Any = solver.Solve()

    if status == Solver.OPTIMAL or status == Solver.FEASIBLE:
        print("Solution: OK")
        print("Objective value =", solver.Objective().Value())
        print("=============================================")
        for i in range(3):
            for j in range(4):
                if amount[i, j].SolutionValue() > 0:
                    print(i, j, amount[i, j].SolutionValue())
        print("Time = ", solver.WallTime(), " milliseconds")
    else:
        print("The problem does not have an optimal solution.")


def get_quantity_carried_out(amount: Dict) -> Tuple[int, int, int]:
    amount_w1: int = 0
    amount_w2: int = 0
    amount_w3: int = 0

    for j in range(4):
        amount_w1 += amount[0, j]
        amount_w2 += amount[1, j]
        amount_w3 += amount[2, j]

    return (amount_w1, amount_w2, amount_w3)


def get_quantity_carried_in(amount: Dict) -> Tuple[int, int, int, int]:
    amount_f1: int = 0
    amount_f2: int = 0
    amount_f3: int = 0
    amount_f4: int = 0

    for i in range(3):
        amount_f1 += amount[i, 0]
        amount_f2 += amount[i, 1]
        amount_f3 += amount[i, 2]
        amount_f4 += amount[i, 3]

    return (amount_f1, amount_f2, amount_f3, amount_f4)


if __name__ == "__main__":
    solve_problem()

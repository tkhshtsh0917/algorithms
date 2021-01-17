from typing import Any, List

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel, CpSolver

LIMIT: int = 9
K_BASE: int = 10


def solve_cryptarithmetic_puzzle() -> bool:
    try:
        model: CpModel = create_model()

        letters: List = create_letters(model)
        add_constraints(model, letters)

        solver: CpSolver = create_solver()
        status: Any = solve_problem(model, solver)

        print_status(solver, letters, status)

    except Exception:
        return False

    return True


def create_model() -> CpModel:
    return cp_model.CpModel()


def create_letters(model: CpModel) -> List:
    s = create_variable(model, 1, "S")
    e = create_variable(model, 0, "E")
    n = create_variable(model, 0, "N")
    d = create_variable(model, 0, "D")
    m = create_variable(model, 1, "M")
    o = create_variable(model, 0, "O")
    r = create_variable(model, 0, "R")
    y = create_variable(model, 0, "Y")

    letters: List = [s, e, n, d, m, o, r, y]
    assert K_BASE >= len(letters)

    return letters


def create_variable(model: CpModel, lower_bound: int, name: str) -> Any:
    return model.NewIntVar(lower_bound, LIMIT, name)


def add_constraints(model: CpModel, letters: List) -> None:
    model.AddAllDifferent(letters)

    [s, e, n, d, m, o, r, y] = letters
    model.Add(
        s * K_BASE * K_BASE * K_BASE
        + e * K_BASE * K_BASE
        + n * K_BASE
        + d
        + m * K_BASE * K_BASE * K_BASE
        + o * K_BASE * K_BASE
        + r * K_BASE
        + e
        == m * K_BASE * K_BASE * K_BASE * K_BASE
        + o * K_BASE * K_BASE * K_BASE
        + n * K_BASE * K_BASE
        + e * K_BASE
        + y
    )


def create_solver() -> CpSolver:
    return cp_model.CpSolver()


def solve_problem(model: CpModel, solver: CpSolver) -> Any:
    return solver.Solve(model)


def print_status(solver: CpSolver, letters: List, status: Any) -> None:
    if solver.StatusName(status) == "OPTIMAL":
        [s, e, n, d, m, o, r, y] = get_solved_values(solver, letters)
        send: str = f"{s} {e} {n} {d}"
        more: str = f"{m} {o} {r} {e}"
        money: str = f"{m} {o} {n} {e} {y}"

        print("<Problem>")
        print("    S E N D")
        print("+ ) M O R E")
        print("-----------")
        print("  M O N E Y")

        print("\n===========\n")

        print("<Answer>")
        print(f"    {send}")
        print(f"+ ) {more}")
        print("-----------")
        print(f"  {money}")


def get_solved_values(solver: CpSolver, letters: List) -> List[int]:
    return list(solver.Value(letter) for letter in letters)


if __name__ == "__main__":
    solve_cryptarithmetic_puzzle()

from Solver.puzzle import Puzzle, Island
from Solver.algorithms import solve_backtracking
from Solver.validator import is_complete_solution


def test_solver_finds_solution():
    puzzle = Puzzle(
        rows=1,
        columns=2,
        islands=[
            Island(0, 0, 0, 1),
            Island(1, 0, 1, 1),
        ],
    )

    solution = solve_backtracking(puzzle)

    assert solution is not None
    assert is_complete_solution(puzzle, solution)


def test_solver_returns_none_when_no_solution():
    puzzle = Puzzle(
    rows=1,
    columns=2,
    islands=[
    Island(0, 0, 0, 1),
    Island(1, 0, 1, 2),
    ],
    )

    solution = solve_backtracking(puzzle)

    assert solution is None
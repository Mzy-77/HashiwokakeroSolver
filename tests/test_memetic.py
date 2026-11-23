from hashiwokakero.Solver.puzzle import Puzzle, Island
from hashiwokakero.Solver.algorithms import memeticSolver
from hashiwokakero.Solver.validator import is_complete_solution
import pytest 

def test_memetic_solver_finds_simple_solution():
    puzzle = Puzzle(
        rows=1,
        columns=2,
        islands=[
            Island(0, 0, 0, 1),
            Island(1, 0, 1, 1),
        ],
    )

    result = memeticSolver(puzzle)

    assert result is not None
    assert is_complete_solution(puzzle, result)


def test_memetic_solver_rejects_impossible_puzzle():
    puzzle = Puzzle(
        rows=1,
        columns=2,
        islands=[
            Island(0, 0, 0, 1),
            Island(1, 0, 1, 2),
        ],
    )

    result = memeticSolver(puzzle)

    assert result is None


def test_memetic_solver_invalid_population_size():
    puzzle = Puzzle(1, 2, [
        Island(0, 0, 0, 1),
        Island(1, 0, 1, 1),
    ])

    with pytest.raises(ValueError):
        memeticSolver(puzzle, population_size=1)


def test_memetic_solver_invalid_local_search_rate():
    puzzle = Puzzle(1, 2, [
        Island(0, 0, 0, 1),
        Island(1, 0, 1, 1),
    ])

    with pytest.raises(ValueError):
        memeticSolver(puzzle, local_search_rate=1.5)
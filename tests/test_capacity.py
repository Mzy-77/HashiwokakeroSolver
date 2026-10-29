from Solver.capacity import hasRemainingCapacity
from Solver.puzzle import Puzzle, Island, Bridge



def test_unassigned_candidate_has_capacity():
    puzzle = Puzzle(
        rows=1,
        columns=2,
        islands=[
            Island(0, 0, 0, 2),
            Island(1, 0, 1, 2),
        ],
    )

    candidates = [(0, 1)]

    assert hasRemainingCapacity(
        puzzle,
        candidates,
        [],
    )


def test_single_bridge_leaves_one_capacity():
    puzzle = Puzzle(
        rows=1,
        columns=2,
        islands=[
            Island(0, 0, 0, 2),
            Island(1, 0, 1, 2),
        ],
    )

    candidates = [(0, 1)]
    bridges = [Bridge(0, 1, 1)]

    assert hasRemainingCapacity(
        puzzle,
        candidates,
        bridges,
    )


def test_double_bridge_leaves_no_capacity():
    puzzle = Puzzle(
        rows=1,
        columns=2,
        islands=[
            Island(0, 0, 0, 2),
            Island(1, 0, 1, 2),
        ],
    )

    candidates = [(0, 1)]
    bridges = [Bridge(0, 1, 2)]

    assert hasRemainingCapacity(
        puzzle,
        candidates,
        bridges,
    )


def test_insufficient_remaining_capacity():
    puzzle = Puzzle(
        rows=1,
        columns=2,
        islands=[
            Island(0, 0, 0, 3),
            Island(1, 0, 1, 3),
        ],
    )

    candidates = [(0, 1)]
    bridges = [Bridge(0, 1, 1)]

    assert not hasRemainingCapacity(
        puzzle,
        candidates,
        bridges,
    )
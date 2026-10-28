from Solver.puzzle import Island
from Solver.candidates import FindCondidates

def test_horizontal_connection():
    islands = [
        Island(0, 0, 0, 1),
        Island(1, 0, 3, 1),
    ]

    assert FindCondidates(islands) == [(0, 1)]


def test_vertical_connection():
    islands = [
        Island(0, 0, 1, 1),
        Island(1, 3, 1, 1),
    ]

    assert FindCondidates(islands) == [(0, 1)]


def test_middle_island_blocks_direct_connection():
    islands = [
        Island(0, 0, 0, 1),
        Island(1, 0, 2, 2),
        Island(2, 0, 4, 1),
    ]

    assert FindCondidates(islands) == [(0, 1), (1, 2)]


def test_diagonal_islands_cannot_connect():
    islands = [
        Island(0, 0, 0, 1),
        Island(1, 2, 2, 1),
    ]

    assert FindCondidates(islands) == []
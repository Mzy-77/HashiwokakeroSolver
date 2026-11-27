import pytest

from hashiwokakero.Solver.puzzle import Island, Puzzle


def test_valid_puzzle():
    puzzle = Puzzle(
        rows=2,
        columns=2,
        islands=[
            Island(0, 0, 0, 1),
            Island(1, 0, 1, 1),
        ],
    )

    puzzle.validate()


def test_empty_puzzle_is_rejected():
    puzzle = Puzzle(rows=2, columns=2, islands=[])

    with pytest.raises(ValueError, match="must contain islands"):
        puzzle.validate()


def test_non_positive_dimensions_are_rejected():
    puzzle = Puzzle(
        rows=0,
        columns=2,
        islands=[Island(0, 0, 0, 1)],
    )

    with pytest.raises(ValueError, match="dimensions must be positive"):
        puzzle.validate()


def test_duplicate_island_ids_are_rejected():
    puzzle = Puzzle(
        rows=2,
        columns=2,
        islands=[
            Island(0, 0, 0, 1),
            Island(0, 1, 1, 1),
        ],
    )

    with pytest.raises(ValueError, match="IDs must be unique"):
        puzzle.validate()


def test_negative_island_id_is_rejected():
    puzzle = Puzzle(
        rows=2,
        columns=2,
        islands=[Island(-1, 0, 0, 1)],
    )

    with pytest.raises(ValueError, match="IDs must be unique"):
        puzzle.validate()


def test_out_of_bounds_row_is_rejected():
    puzzle = Puzzle(
        rows=2,
        columns=2,
        islands=[Island(0, 2, 0, 1)],
    )

    with pytest.raises(ValueError, match="Invalid row"):
        puzzle.validate()


def test_out_of_bounds_column_is_rejected():
    puzzle = Puzzle(
        rows=2,
        columns=2,
        islands=[Island(0, 0, 2, 1)],
    )

    with pytest.raises(ValueError, match="Invalid column"):
        puzzle.validate()


def test_duplicate_island_positions_are_rejected():
    puzzle = Puzzle(
        rows=2,
        columns=2,
        islands=[
            Island(0, 0, 0, 1),
            Island(1, 0, 0, 2),
        ],
    )

    with pytest.raises(ValueError, match="same cell"):
        puzzle.validate()


@pytest.mark.parametrize("required", [0, 9, -1])
def test_invalid_island_requirement_is_rejected(required):
    puzzle = Puzzle(
        rows=2,
        columns=2,
        islands=[Island(0, 0, 0, required)],
    )

    with pytest.raises(ValueError, match="between 1 and 8"):
        puzzle.validate()

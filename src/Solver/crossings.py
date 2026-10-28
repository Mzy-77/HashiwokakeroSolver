from Solver.puzzle import Puzzle , Bridge

def bridges_cross(
    puzzle: Puzzle,
    first: Bridge,
    second: Bridge,
) -> bool:
    

    islands = {island.id: island for island in puzzle.islands}


    for bridge in (first, second):
        if bridge.island_a not in islands or bridge.island_b not in islands:
            raise ValueError("Bridge references an unknown island.")

    a = islands[first.island_a]
    b = islands[first.island_b]
    c = islands[second.island_a]
    d = islands[second.island_b]


    if a.row != b.row and a.column != b.column:
        raise ValueError("Bridges must be horizontal or vertical.")

    if c.row != d.row and c.column != d.column:
        raise ValueError("Bridges must be horizontal or vertical.")


    first_horizontal = a.row == b.row
    second_horizontal = c.row == d.row
    if first_horizontal == second_horizontal:
        return False

    if first_horizontal:
        horizontal_row = a.row
        horizontal_left = min(a.column, b.column)
        horizontal_right = max(a.column, b.column)
        vertical_col = c.column
        vertical_top = min(c.row, d.row)
        vertical_bottom = max(c.row, d.row)
    else:
        horizontal_row = c.row
        horizontal_left = min(c.column, d.column)
        horizontal_right = max(c.column, d.column)
        vertical_col = a.column
        vertical_top = min(a.row, b.row)
        vertical_bottom = max(a.row, b.row)

    # The intersection must be strictly inside both bridges.
    return (
        horizontal_left < vertical_col < horizontal_right
        and vertical_top < horizontal_row < vertical_bottom
    )


def has_crossings(
    puzzle: Puzzle,
    bridges: list[Bridge],
) -> bool:

    for i in range(len(bridges)):
        for j in range(i + 1, len(bridges)):
            if bridges_cross(puzzle, bridges[i], bridges[j]):
                return True

    return False
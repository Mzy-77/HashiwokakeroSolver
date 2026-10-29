from Solver.puzzle import Puzzle ,Bridge



def hasRemainingCapacity(
    puzzle: Puzzle,
    candidates: list[tuple[int, int]],
    bridges: list[Bridge],
) -> bool:
    islands = {island.id: island for island in puzzle.islands}
    current_counts = {island.id: 0 for island in puzzle.islands}
    remaining_capacity = {island.id: 0 for island in puzzle.islands}

    assigned_pairs = {}

    for bridge in bridges:
        if bridge.island_a not in islands or bridge.island_b not in islands:
            raise ValueError("Bridge references an unknown island.")

        pair = tuple(sorted((bridge.island_a, bridge.island_b)))
        assigned_pairs[pair] = bridge.count

        current_counts[bridge.island_a] += bridge.count
        current_counts[bridge.island_b] += bridge.count

    for island_a, island_b in candidates:
        if island_a not in islands or island_b not in islands:
            raise ValueError("Candidate references an unknown island.")

        pair = tuple(sorted((island_a, island_b)))
        assigned_count = assigned_pairs.get(pair, 0)

        remaining = 2 - assigned_count

        remaining_capacity[island_a] += remaining
        remaining_capacity[island_b] += remaining

    for island in puzzle.islands:
        possible_total = (
            current_counts[island.id]
            + remaining_capacity[island.id]
        )

        if possible_total < island.required:
            return False

    return True
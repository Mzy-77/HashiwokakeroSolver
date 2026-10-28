from Solver.puzzle import Puzzle , Bridge

def hasRemainingCapacity(puzzle: Puzzle, candidates: list[tuple[int, int]], bridges: list[Bridge])->bool:
    islands = {island.id: island for island in puzzle.islands}
    current_counts = {island.id : 0 for island in puzzle.islands}
    remaining_capacity = {island.id : 0 for island in puzzle.islands}

    for bridge in bridges :
        if bridge.island_a not in islands or bridge.island_b not in islands:
            raise ValueError("Bridge references an unknown island.")

        current_counts[bridge.island_a] =+ bridge.count
        current_counts[bridge.island_b] =+ bridge.count

    pairs = {(bridge.island_a , bridge.island_b ) for bridge in bridges}

    for island_a , island_b in candidates:
        pair = tuple(sorted((island_a, island_b)))

        if pair in pairs:
            continue

        if island_a not in islands or island_b not in islands : raise ValueError("Bridge references an unknown island.")
        remaining_capacity[island_a] =+ 2
        remaining_capacity[island_b] =+ 2

    for island in puzzle.islands:
        possibaleTotal = (
            current_counts[island.id] + remaining_capacity[island.id]
        )
        if possibaleTotal < island.required:
            return False 
    return True
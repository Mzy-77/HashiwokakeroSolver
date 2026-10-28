from Solver.puzzle import Puzzle , Bridge

def getBridgeCount(
        puzzle: Puzzle ,
        bridges: list[Bridge],
)-> dict[int, int ]:
    counts = {island.id: 0 for island in puzzle.islands}

    for bridge in bridges:
        if bridge.island_a not in counts or bridge.island_b not in counts:
            raise ValueError("Bridge references an unknown island.")

        counts[bridge.island_a] += bridge.count
        counts[bridge.island_b] += bridge.count


    return counts

def isBridgeCountsValid(
    puzzle: Puzzle,
    bridges: list[Bridge],
) -> bool:
    counts = getBridgeCount(puzzle, bridges)

    required = {
        island.id: island.required for island in puzzle.islands
    }

    return all(
        counts[island_id] <= required[island_id] for island_id in counts
    )

def bridgeCountComplete(
        puzzle: Puzzle,
        bridges: list[Bridge],
)-> bool:
    counts = getBridgeCount(puzzle, bridges)

    required = {
        island.id: island.required
        for island in puzzle.islands
    }

    return counts == required

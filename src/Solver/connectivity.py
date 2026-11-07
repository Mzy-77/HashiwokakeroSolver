from Solver.puzzle import Puzzle , Bridge
def isConnected(
        puzzle :Puzzle,
        bridges:list[Bridge]
)-> bool :
    if not puzzle.islands: return False

    graph: dict[int, list[int]] = {island.id: [] for island in puzzle.islands}

    for bridge in bridges :
        if bridge.island_a not in graph or bridge.island_b not in graph : raise ValueError("Bridge references an unknown island.")

        graph[bridge.island_a].append(bridge.island_b)
        graph[bridge.island_b].append(bridge.island_a)

    start = puzzle.islands[0].id
    visited: set[int] = set()
    stack: list[int] = [start]

    while stack:
        current  = stack.pop()

        if current in visited :
            continue

        visited.add(current)

        for neighbor in graph[current]:
            if neighbor not in visited :
                stack.append(neighbor)

    return len(visited) == len(puzzle.islands)

def countComponents(puzzle: Puzzle, bridges: list[Bridge]) -> int:
    if not puzzle.islands:
        return 0

    graph: dict[int, list[int]] = {island.id: [] for island in puzzle.islands}

    for bridge in bridges:
        if bridge.island_a not in graph or bridge.island_b not in graph:
            raise ValueError("Bridge references an unknown island.")

        graph[bridge.island_a].append(bridge.island_b)
        graph[bridge.island_b].append(bridge.island_a)

    visited: set[int] = set()
    components = 0

    for island in puzzle.islands:
        if island.id not in visited:
            components += 1
            stack: list[int] = [island.id]

            while stack:
                current = stack.pop()

                if current in visited:
                    continue

                visited.add(current)

                for neighbor in graph[current]:
                    if neighbor not in visited:
                        stack.append(neighbor)

    return components
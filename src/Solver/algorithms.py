from Solver.puzzle import Puzzle , Bridge




def backTrackingSolver(puzzle: Puzzle , bridges:list[Bridge]):
    return None

def geneticSolver(puzzle: Puzzle, bridges:list[Bridge]):
    return None

def memeticSolver(puzzle: Puzzle, bridges:list[Bridge]):
    return None

"Depth First Search"
def isConnected(
        puzzle :Puzzle,
        bridges:list[Bridge]
)-> bool :
    if not puzzle.islands: return False

    graph = {island.id: [] for island in puzzle.islands}

    for bridge in bridges :
        if bridge.island_a not in graph or bridge.island_b not in graph : raise ValueError("Bridge references an unknown island.")

        graph[bridge.island_a].append(bridge.island_b)
        graph[bridge.island_b].append(bridge.island_a)

    start = puzzle.islands[0].id
    visited = set()
    stack= [start]

    while stack:
        current  = stack.pop()

        if current in visited :
            continue

        visited.add(current)

        for neighbor in graph[current]:
            if neighbor not in visited :
                stack.append(neighbor)

    return len(visited) == len(puzzle.islands)
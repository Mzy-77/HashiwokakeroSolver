from Solver.puzzle import Puzzle , Bridge
from Solver.candidates import FindCandidates
from Solver.validator import is_complete_solution
from Solver.capacity import hasRemainingCapacity
from Solver.connectivity import countComponents
from Solver.constraints import getBridgeCount 
from Solver.crossings import has_crossings
from random import randint



def solve_backtracking(puzzle: Puzzle) -> list[Bridge] | None:
    candidates = FindCandidates(puzzle.islands)

    def backTrack(index: int, bridges: list[Bridge]) -> list[Bridge] | None:
        if not hasRemainingCapacity(puzzle, candidates[index:], bridges): return None

        if index == len(candidates):
            if is_complete_solution(puzzle, bridges):
                return bridges
            return None
        
        island_a , island_b = candidates[index]

        result = backTrack(index + 1, bridges)
        if result is not None :
                    return result
        
        single_bridge = Bridge(island_a, island_b, 1)

        result = backTrack(index + 1, bridges + [single_bridge])
        if result is not None :
            return result

        double_bridge = Bridge(island_a, island_b, 2)
        result = backTrack(index + 1, bridges + [double_bridge])
        if result is not None : return result

        return None

    return backTrack(0, [])

def genome(count: int) -> list[int]:
    return [randint(0, 2) for _ in range(count)]

def population(size: int, count: int) -> list[list[int]]:
    if size <= 0 or count <= 0:
        raise ValueError("Size and count must be positive integers.")
    return [genome(count) for _ in range(size)]

def asignBridges(genome: list[int], candidates: list[tuple[int, int]]) -> list[Bridge]:
    if len(candidates) != len(genome):
        raise ValueError("Candidates and genome must have the same length.")

    bridges: list[Bridge] = []

    for gene, (island_a, island_b) in zip(genome, candidates):
        if gene not in (0, 1, 2):
            raise ValueError("Gene values must be 0, 1, or 2.")
        if gene == 0:
            continue
        bridges.append(Bridge(island_a, island_b, gene))
    return bridges

def fitness(puzzle: Puzzle, bridges:list[Bridge])-> int:
    bridge_count: dict[int, int] = getBridgeCount(puzzle, bridges)
    degree_penalty = sum(
        abs(island.required - bridge_count.get(island.id, 0))
        for island in puzzle.islands
    )
    crossing_penalty = 3 if has_crossings(puzzle, bridges) else 0
    components = countComponents(puzzle, bridges)
    connectivity_penalty = 3 * max(0, components - 1)
    return degree_penalty + crossing_penalty + connectivity_penalty

def memeticSolver(puzzle: Puzzle):
    return None


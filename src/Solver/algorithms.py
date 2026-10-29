from Solver.puzzle import Puzzle , Bridge
from Solver.candidates import FindCandidates
from Solver.validator import is_complete_solution
from Solver.capacity import hasRemainingCapacity


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


def geneticSolver(puzzle: Puzzle, bridges:list[Bridge]):
    return None

def memeticSolver(puzzle: Puzzle):
    return None


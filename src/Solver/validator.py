from Solver.puzzle import Puzzle , Bridge
from Solver.constraints import bridgeCountComplete , isBridgeCountsValid

from Solver.crossings import has_crossings
from Solver.connectivity import isConnected

def isValidState(
        puzzle: Puzzle,
        bridges: list[Bridge]
) -> bool:
    if not isBridgeCountsValid(puzzle, bridges):
        return False
    if has_crossings(puzzle, bridges):
        return False

    return True

def is_complete_solution(puzzle: Puzzle, bridges: list[Bridge])-> bool :
    if not isValidState(puzzle, bridges):
        return False

    if not bridgeCountComplete(puzzle, bridges):
        return False

    if not isConnected(puzzle, bridges):
        return False

    return True


import pytest 
from Solver.puzzle import Puzzle, Bridge, Island
from Solver.constraints import (
    getBridgeCount,
    bridgeCountComplete,
    isBridgeCountsValid
)

@pytest.fixture
def puzzle():
    return Puzzle(rows=3, columns= 3 , islands=[Island(0,1,0,2), Island(1, 1, 2, 2)],)



def test_get_bridge_counts(puzzle):
    bridges = [Bridge(0, 1)]

    assert getBridgeCount(puzzle, bridges) == {
        0: 1,
        1: 1,
    }


def test_bridge_counts_valid(puzzle):
    bridges = [Bridge(0, 1)]

    assert isBridgeCountsValid(puzzle, bridges)


def test_bridge_counts_complete(puzzle):
    bridges = [Bridge(0, 1, 2)]

    assert bridgeCountComplete(puzzle, bridges)


def test_bridge_counts_invalid(puzzle):
    bridges = [Bridge(0, 1, 2), Bridge(0, 1)]

    assert not isBridgeCountsValid(puzzle, bridges)


def test_unknown_island_raises_error(puzzle):
    bridges = [Bridge(0, 99)]

    with pytest.raises(ValueError):
        getBridgeCount(puzzle, bridges)
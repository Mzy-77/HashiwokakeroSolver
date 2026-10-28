
import pytest

from Solver.puzzle import Bridge


def test_single_bridge():
    bridge = Bridge(0, 1)
    assert bridge.island_a == 0
    assert bridge.island_b == 1
    assert bridge.count == 1


def test_double_bridge():
    bridge = Bridge(0, 1, 2)
    assert bridge.count == 2


def test_bridge_order_is_normalized():
    bridge = Bridge(5, 2)
    assert bridge.island_a == 2
    assert bridge.island_b == 5


def test_bridge_cannot_connect_island_to_itself():
    with pytest.raises(ValueError):
        Bridge(1, 1)


def test_invalid_bridge_count():
    with pytest.raises(ValueError):
        Bridge(0, 1, 3)

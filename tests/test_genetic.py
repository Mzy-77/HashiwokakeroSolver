
from Solver.algorithms import (
    genome,
    population,
    asignBridges,
)
from Solver.puzzle import Puzzle, Bridge ,Island
from Solver.connectivity import countComponents

def test_chromosome_length():
    chromosome = genome(5)

    assert len(chromosome) == 5

def test_components_count():
    
    a = Island(0, 0, 0, 1)
    b = Island(1, 0, 1, 1)
    c = Island(2, 1, 0, 1)

    puzzle = Puzzle(2, 2, [a, b, c])

    bridges = [
        Bridge(0, 1, 1)
    ]

    assert countComponents(puzzle, bridges) == 2

def test_chromosome_values():
    chromosome = genome(10)

    assert all(gene in (0, 1, 2) for gene in chromosome)


def test_population_size():
    Population = population(5, 20)

    assert len(Population) == 5
    assert all(len(c) == 20 for c in Population)


def test_chromosome_to_bridges():
    candidates = [
        (0, 1),
        (0, 2),
    ]

    chromosome = [2, 0]

    bridges = asignBridges(
        chromosome,
        candidates,
    )

    assert len(bridges) == 1
    assert bridges[0].count == 2


def test_invalid_chromosome_length():
    candidates = [
        (0, 1)
    ]

    try:
        asignBridges([1, 2], candidates)
        assert False
    except ValueError:
        assert True

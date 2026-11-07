
from Solver.algorithms import (

    selection,
    corssover,
    mutation,
)


def test_selection():
    population = [
        [0, 0, 0],
        [1, 1, 1],
        [2, 2, 2],
    ]

    scores = [10, 0, 20]

    winner = selection(population, scores, 3)

    assert winner == [1, 1, 1]


def test_crossover():
    parent_a = [0, 0, 0, 0]
    parent_b = [2, 2, 2, 2]

    child_a, child_b = corssover(parent_a, parent_b)

    assert len(child_a) == 4
    assert len(child_b) == 4
    assert all(gene in (0, 1, 2) for gene in child_a + child_b)


def test_mutation():
    chromosome = [0, 0, 0, 0]

    mutated = mutation(chromosome, 1.0)

    assert all(gene in (0, 1, 2) for gene in mutated)
    assert chromosome == [0, 0, 0, 0]


def test_mutation_zero_rate():
    chromosome = [0, 1, 2]

    mutated = mutation(chromosome, 0)

    assert mutated == chromosome
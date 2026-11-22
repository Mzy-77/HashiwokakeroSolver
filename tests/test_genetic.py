
from hashiwokakero.Solver.algorithms import (

    selection,
    corssover,
    mutation,
    asignBridges,
    localSearch,
    fitness,
)
from hashiwokakero.Solver.puzzle import Island, Puzzle
from hashiwokakero.Solver.validator import is_complete_solution


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



def test_local_search_preserves_chromosome_length():

    a = Island(0, 0, 0, 1)
    b = Island(1, 0, 1, 1)

    puzzle = Puzzle(1, 2, [a, b])
    candidates = [(a.id, b.id)]

    chromosome = [0]

    result = localSearch(
        puzzle,
        chromosome,
        candidates,
    )

    assert len(result) == len(chromosome)


def test_local_search_never_worsens_fitness():

    a = Island(0, 0, 0, 1)
    b = Island(1, 0, 1, 1)

    puzzle = Puzzle(1, 2, [a, b])
    candidates = [(a.id, b.id)]

    chromosome = [0]

    original_score = fitness(
        puzzle,
        asignBridges(chromosome, candidates)
    )

    result = localSearch(
        puzzle,
        chromosome,
        candidates,
    )

    improved_score = fitness(
        puzzle,
        asignBridges(result, candidates)
    )

    assert improved_score <= original_score
    assert chromosome == [0]


def test_local_search_finds_simple_solution():

    a = Island(0, 0, 0, 1)
    b = Island(1, 0, 1, 1)

    puzzle = Puzzle(1, 2, [a, b])
    candidates = [(a.id, b.id)]

    result = localSearch(
        puzzle,
        [0],
        candidates,
    )

    bridges = asignBridges(result, candidates)

    assert is_complete_solution(puzzle, bridges)

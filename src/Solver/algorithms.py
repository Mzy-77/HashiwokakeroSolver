from Solver.puzzle import Puzzle , Bridge
from Solver.candidates import FindCandidates
from Solver.validator import is_complete_solution
from Solver.capacity import hasRemainingCapacity
from Solver.connectivity import countComponents
from Solver.constraints import getBridgeCount 
from Solver.crossings import has_crossings
import random



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

"genetic algorithms satart here"

def genome(count: int) -> list[int]:
    return [random.randint(0, 2) for _ in range(count)]

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

def selection(population: list[list[int]],  scores: list[int], tourament_size: int = 3 ) -> list[int]:
    indexes: list[int] = random.sample(
        range(len(population)),(min(tourament_size, len(population)))
    )

    winner : int = min(indexes, key=lambda i: scores[i])

    return population[winner].copy()

def corssover(parent1: list[int], parent2: list[int])-> tuple[list[int], list[int]]:
    if len(parent1) != len(parent2):
        raise ValueError("Parents must have the same length.")
    if len(parent1) < 2:
        return parent1.copy(), parent2.copy()
    
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2

def mutation(genome: list[int], mutation_rate: float = 0.05) -> list[int]:
    if not (0 <= mutation_rate <= 1):
        raise ValueError("Mutation rate must be between 0 and 1.")
    
    mutated_genome = genome.copy()
    for i in range(len(mutated_genome)):
        if random.random() < mutation_rate:
            mutated_genome[i] = random.randint(0, 2)
    return mutated_genome


def geneticSolver(
        puzzle: Puzzle,
        population_size: int = 100,
        max_generations: int = 500,
        mutation_rate: float = 0.05,
        elitism_size: int = 2,
        )-> list[Bridge] | None:

    canadidates = FindCandidates(puzzle.islands)
    # if not canadidates:
    #     return []

    if is_complete_solution(puzzle, []):
        return []

    if population_size <= 0 or max_generations <= 0 or not (0 <= mutation_rate <= 1) or elitism_size < 0:
        raise ValueError("Invalid parameters for genetic algorithm.")

    current_population: list[list[int]] = population(population_size, len(canadidates))
    best_genome: list[int] | None = None
    best_score: float = float('inf')

    for generation in range(max_generations):
        scores : list[int]= [
            fitness(puzzle, asignBridges(genome, canadidates)) for genome in current_population
        ]

        best_index= min(range(len(scores)), key=lambda i: scores[i])
        if scores[best_index] < best_score:
            best_score = scores[best_index]
            best_genome = current_population[best_index].copy()

        for genome in current_population:
            brides =  asignBridges(genome, canadidates)
            return brides


    return None


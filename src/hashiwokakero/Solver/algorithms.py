from hashiwokakero.Solver.puzzle import Puzzle , Bridge
from hashiwokakero.Solver.candidates import FindCandidates
from hashiwokakero.Solver.validator import is_complete_solution
from hashiwokakero.Solver.capacity import hasRemainingCapacity
from hashiwokakero.Solver.connectivity import countComponents
from hashiwokakero.Solver.constraints import getBridgeCount 
from hashiwokakero.Solver.crossings import has_crossings
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
        elitism_count: int = 2,
        )-> list[Bridge] | None:

    canadidates = FindCandidates(puzzle.islands)
    # if not canadidates:
    #     return []

    if is_complete_solution(puzzle, []):
        return []

    if population_size <= 0 or max_generations <= 0 or not (0 <= mutation_rate <= 1) or elitism_count < 0:
        raise ValueError("Invalid parameters for genetic algorithm.")

    current_population: list[list[int]] = population(population_size, len(canadidates))
    best_genome: list[int] | None = None
    best_score: float = float('inf')

    for _ in range(max_generations):


        scores : list[int]= [
            fitness(puzzle, asignBridges(genome, canadidates)) for genome in current_population
        ]

        best_index= min(range(len(scores)), key=lambda i: scores[i])

        if scores[best_index] < best_score:

            best_score = scores[best_index]
            best_genome = current_population[best_index].copy()

        for genome in current_population:
            brides =  asignBridges(genome, canadidates)
            if is_complete_solution(puzzle, brides):
                return brides

        ranked_indexes: list[int] = sorted(range(len(scores)), key=lambda i: scores[i])

        next_population: list[list[int]] = [
            current_population[i].copy() for i in ranked_indexes[:elitism_count]
        ]

        while len(next_population) < population_size: 
            parent1 = selection(current_population, scores)
            parent2 = selection(current_population, scores)

            child1, child2 = corssover(parent1, parent2)

            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)

            next_population.append(child1)

            if len(next_population) < population_size:
                next_population.append(child2)

        current_population = next_population

    if best_genome is not None:
        return asignBridges(best_genome, canadidates)

    return None

"end"

def localSearch(
    puzzle: Puzzle,
    chromosome: list[int],
    candidates: list[tuple],
    max_steps: int = 50,
) -> list[int]:

    if max_steps < 0:
        raise ValueError("max_steps cannot be negative")

    best = chromosome.copy()

    best_score = fitness(
        puzzle,
        asignBridges(best, candidates)
    )

    for _ in range(max_steps):

        improved = False

        for i in range(len(best)):

            for value in (0, 1, 2):

                if value == best[i]:
                    continue

                neighbor = best.copy()
                neighbor[i] = value

                neighbor_score = fitness(
                    puzzle,
                    asignBridges(neighbor, candidates)
                )

                if neighbor_score < best_score:

                    best = neighbor
                    best_score = neighbor_score
                    improved = True

        if is_complete_solution(
            puzzle,
            asignBridges(best, candidates)
        ):
            return best

        if not improved:
            break

    return best

def memeticSolver(
    puzzle: Puzzle,
    population_size: int = 100,
    max_generations: int = 500,
    mutation_rate: float = 0.05,
    elitism_count: int = 2,
    local_search_rate: float = 0.2,
    local_search_steps: int = 20,
) -> list[Bridge] | None:

    candidates = FindCandidates(puzzle.islands)

    if is_complete_solution(puzzle, []):
        return []

    if population_size < 2:
        raise ValueError("Population size must be at least 2")

    if max_generations < 1:
        raise ValueError("Maximum generations must be at least 1")

    if not 1 <= elitism_count < population_size:
        raise ValueError("Elitism count must be between 1 and population_size - 1")

    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1")

    if not 0 <= local_search_rate <= 1:
        raise ValueError("Local search rate must be between 0 and 1")

    if local_search_steps < 0:
        raise ValueError("Local search steps cannot be negative")

    current_population = population(population_size, len(candidates))

    best_genome = None
    best_score = float("inf")
    
    for generation in range(max_generations):
        scores = [
            fitness(puzzle, asignBridges(chromosome, candidates))
            for chromosome in current_population
        ]

        for chromosome, score in zip(current_population, scores):

            bridges = asignBridges(chromosome, candidates)

            if is_complete_solution(puzzle, bridges):
                return bridges

            if score < best_score:
                best_score = score
                best_genome = chromosome.copy

        ranked_population = sorted(
            zip(current_population, scores),
            key=lambda individual: individual[1]
        )

        next_population = [
            chromosome.copy()
            for chromosome, _ in ranked_population[:elitism_count]
        ]

        while len(next_population) < population_size :

            parent1 = selection(current_population, scores)
            parent2 = selection(current_population, scores)

            child1 , child2 = corssover(parent1, parent2)
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)

            offspring = [child1, child2]

            for child in offspring:
                if len(next_population)>= population_size:
                    break

                if random.random()< local_search_rate:
                    child = localSearch(
                        puzzle,
                        child,
                        candidates,
                        local_search_steps
                    )

                bridges = asignBridges(child, candidates)

                if is_complete_solution(puzzle, bridges):
                    return bridges

                next_population.append(child)

            current_population = next_population

        if best_genome is not None:
            bridges = asignBridges(best_genome, candidates)

            if is_complete_solution(puzzle, bridges):
                return bridges

        return None

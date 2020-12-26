from collections import namedtuple
from random import choice, choices, randint, random, randrange
from typing import List, Tuple, Callable

Edge = namedtuple('Edge', ['src', 'dst', 'weight'])
Graph = dict
Genome = List[Edge]
Population = List[Genome]
PopulationFunc = Callable[[int, Graph], Population]
FitnessFunc = Callable[[Genome, Graph], float]
SelectionFunc = Callable[[Population, FitnessFunc, Graph], Population]
GraphFunc = Callable[[], Graph]
GenomeFunc = Callable[[Graph], Genome]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome, Graph, float], Genome]


def generate_graph() -> Graph:
    # return {
    #     'A': [Edge('A', 'B', 2), Edge('A', 'C', 9)],
    #     'B': [Edge('B', 'A', 2), Edge('B', 'C', 2), Edge('B', 'D', 6)],
    #     'C': [Edge('C', 'A', 9), Edge('C', 'B', 2), Edge('C', 'D', 3)],
    #     'D': [Edge('D', 'C', 3), Edge('D', 'B', 6)]
    # }
    return {
        'SAC': [Edge('SAC', 'SF', 2), Edge('SAC', 'LA', 6), Edge('SAC', 'TX', 5)],
        'SF': [Edge('SF', 'NY', 8), Edge('SF', 'SAC', 2), Edge('SF', 'TX', 6)],
        'LA': [Edge('LA', 'SAC', 6), Edge('LA', 'NY', 5), Edge('LA', 'TX', 3)],
        'TX': [Edge('TX', 'LA', 3), Edge('TX', 'FL', 4), Edge('TX', 'SAC', 5), Edge('TX', 'SF', 6), Edge('TX', 'NY', 4)],
        'NY': [Edge('NY', 'SF', 8), Edge('NY', 'TX', 4), Edge('NY', 'FL', 3), Edge('NY', 'IC', 5), Edge('NY', 'SW', 7)],
        'FL': [Edge('FL', 'TX', 4), Edge('FL', 'NY', 3), Edge('FL', 'AUS', 14)],
        'IC': [Edge('IC', 'NY', 5)],
        'SW': [Edge('SW', 'NY', 7)],
        'AUS': [Edge('AUS', 'FL', 14)],
    }


def generate_population(size: int, graph: Graph) -> Population:
    population = []
    for _ in range(size):
        population.append(generate_genome(graph))
    return population


def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    min_length = min(len(a), len(b))
    crossover_idx = -1
    while crossover_idx < 0:
        tmp_idx = randint(0, min_length-1)
        crossover_idx = tmp_idx if getattr(a[tmp_idx], 'src') == getattr(b[tmp_idx], 'src') else crossover_idx
    return a[0:crossover_idx] + b[crossover_idx:], b[0:crossover_idx] + a[crossover_idx:]


def selection_pair(population: Population, fitness_func: FitnessFunc, graph: Graph) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(gene, graph) for gene in population],
        k=2
    )


def generate_genome(graph: Graph) -> Genome:
    result = []
    visited_nodes = set()
    root = next(iter(graph))
    while len(visited_nodes) < len(graph):
        edge = choice(graph.get(root))
        result.append(edge)
        visited_nodes.add(getattr(edge, 'src'))
        visited_nodes.add(getattr(edge, 'dst'))
        root = getattr(edge, 'dst')
    return result


def finish_genome(genome: Genome, graph: Graph) -> Genome:
    result = genome
    visited_nodes = set()
    root = next(iter(graph)) if len(genome) == 0 else None
    # iterates incomplete genome and populates visited_nodes
    for edge in genome:
        visited_nodes.add(getattr(edge, 'src'))
        visited_nodes.add(getattr(edge, 'dst'))
        root = getattr(edge, 'dst')
    while len(visited_nodes) < len(graph):
        edge = choice(graph.get(root))
        result.append(edge)
        visited_nodes.add(getattr(edge, 'src'))
        visited_nodes.add(getattr(edge, 'dst'))
        root = getattr(edge, 'dst')
    return result


def mutation(genome: Genome, graph: Graph, probability: float = 0.1) -> Genome:
    if random() > probability:
        return genome
    return finish_genome(genome[0:randrange(1, len(genome))], graph)


def fitness(genome: Genome, graph: Graph) -> float:
    return 0 if not valid_genome(genome, graph) else 100 / sum(c.weight for c in genome)


def valid_genome(genome: Genome, graph: Graph) -> bool:
    visited_nodes = set()
    for edge in genome:
        visited_nodes.add(getattr(edge, 'src'))
        visited_nodes.add(getattr(edge, 'dst'))
    return len(visited_nodes) == len(graph)


def run_evolution(
        graph_func: GraphFunc = generate_graph,
        population_func: PopulationFunc = generate_population,
        fitness_func: FitnessFunc = fitness,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        population_count: int = 20,
        generation_limit: int = 1500):
    graph = graph_func()
    population = population_func(population_count, graph)
    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome, graph), reverse=True)
        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func, graph)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a, graph, .35)
            offspring_b = mutation_func(offspring_b, graph, .35)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

        #debugging
        sorted_genomes = sorted(next_generation, key=lambda genome: fitness_func(genome, graph), reverse=True)
        print(sum(c.weight for c in sorted_genomes[0]), sorted_genomes[0])


run_evolution()

# Traveling Salesman Problem - Genetic Algorithm

This is an implementation of the Traveling Salesman Problem (TSP) using a genetic algorithm. TSP is an optimization problem where the goal is to find the shortest possible route that visits every city in a given list exactly once and returns to the starting city. The genetic algorithm is a heuristic search algorithm inspired by the process of natural selection.

## Installation

Clone the repository to your local machine:

```
git clone https://github.com/dgyurics/evolution.git
```

## Usage

Run the program from the command line using Python:

```
python tsp.py
```

This will generate an optimal path for the given list of cities, based on the genetic algorithm.

## Configuration

You can configure the program by editing the variables at the top of the `tsp.py` file:

```python
POPULATION_SIZE = 100
GENERATIONS = 1000
MUTATION_RATE = 0.1
ELITISM = True
TOURNAMENT_SIZE = 5
```

- `POPULATION_SIZE`: the number of genomes in each generation.
- `GENERATIONS`: the number of generations to run.
- `MUTATION_RATE`: the probability of a mutation occurring in a genome.
- `ELITISM`: whether to keep the fittest genome from each generation in the next generation.
- `TOURNAMENT_SIZE`: the number of genomes to randomly select for the tournament selection process.

You can also configure the list of cities by editing the `generate_graph` function in the `tsp.py` file. Each city should be represented as a node in the graph, and the edges should represent the distances between the cities.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

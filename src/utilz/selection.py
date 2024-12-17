import random
import numpy as np


class Selection(object):
    def __init__(self, selection_algorithm):
        self.selection_algorithm = selection_algorithm

    def select(self, population, fitness_list):
        return self.selection_algorithm(population, fitness_list)


class RouletteSelection(object):
    def __call__(self, population, fitness_list):
        return self.select_pop(population, fitness_list)

    def select_pop(self, population, fitness_list):
        new_population = []

        # Subtract the worst fitness score from all fitness scores to increase the difference between them.
        # This ensures that chromosomes with higher fitness scores have a larger range in the cumulative sum,
        # increasing their probability of being selected.
        worst_fit = np.min(fitness_list)
        fitness_list = [fitness - worst_fit for fitness in fitness_list]

        cumulative_sum = np.cumsum(fitness_list)

        for _ in range(len(population)):
            # Generate a random value in the range (0, sum(fitness))
            random_prob = random.uniform(0, 1) * np.sum(fitness_list)

            # Find the chromosome index that corresponds to the random value in the cumulative sum
            for index in range(len(population)):
                if 0 <= random_prob <= cumulative_sum[index]:
                    new_population.append(population[index])
                    break

        return new_population

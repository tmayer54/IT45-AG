import random

from config import MUTATION_PROBABILITY


class Mutation(object):
    def __init__(self, mutation_algorithm):
        self.mutation_algorithm = mutation_algorithm

    def mutate(self, population):
        return self.mutation_algorithm(population)


class MutationSwitch(object):
    def __call__(self, population):
        return self.mutate_pop(population)

    def mutate_pop(self, population):
        population_mutated = []
        for chromosome in population:
            # Check if mutation should occur based on mutation probability
            if 0 <= random.uniform(0, 1) <= MUTATION_PROBABILITY:
                # Mutate the chromosome
                mutated_chromosome = MutationSwitch.mutate_chr(chromosome, MutationSwitch.gen_index(chromosome))
                population_mutated.append(mutated_chromosome)
            else:
                # No mutation, append the original chromosome
                population_mutated.append(chromosome)
        return population_mutated

    @staticmethod
    def mutate_chr(chromosome, random_indexes):
        """
        Mutates a chromosome by swapping two genes at random indexes.

        Args:
            chromosome (list): Chromosome representation.
            random_indexes (tuple): Random indexes for gene swapping.

        Returns:
            chromosome (list): Mutated chromosome.
        """
        gen_a_index, gen_b_index = random_indexes
        chromosome[gen_a_index], chromosome[gen_b_index] = chromosome[gen_b_index], chromosome[gen_a_index]
        return chromosome

    @staticmethod
    def gen_index(chromosome):
        """
        Generates random indexes for gene swapping within a chromosome.

        Args:
            chromosome (list): Chromosome representation.

        Returns:
            random_indexes (tuple): Random indexes for gene swapping.
        """
        return random.randint(0, len(chromosome) - 1), random.randint(0, len(chromosome) - 1)

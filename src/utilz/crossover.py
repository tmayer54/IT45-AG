import random

from config import CROSSOVER_PROBABILITY

class Crossover(object):
    def __init__(self, crossover_algorithm):
        self.crossover_algorithm = crossover_algorithm

    def crossover(self, population):
        return self.crossover_algorithm(population)

class Crossover2X(object):
    # Callable class
    def __call__(self, population):
        return self.cross_pop(population)

    def cross_pop(self, population):
        chromosome_to_cross = []  # List to store chromosomes to be crossed
        chromosome_not_to_cross = []  # List to store chromosomes not to be crossed

        # Select chromosomes to be crossed and those not to be crossed
        Crossover2X.select_chromosome_to_cross(population, chromosome_to_cross, chromosome_not_to_cross)

        # Generate pairs of chromosomes to be crossed
        chromosome_couples = Crossover2X.generate_couples(chromosome_to_cross, chromosome_not_to_cross)

        # Perform crossover on the chromosome couples
        new_population = Crossover2X.cross_couples(chromosome_couples)

        # Combine the crossed-over chromosomes and the original chromosomes not to be crossed
        return new_population + chromosome_not_to_cross

    @staticmethod
    def select_chromosome_to_cross(population, chromosome_to_cross, chromosome_not_to_cross):
        for chromosome in population:
            # Select chromosomes for crossover based on the CROSSOVER_PROBABILITY
            if 0 <= random.uniform(0, 1) <= CROSSOVER_PROBABILITY:
                chromosome_to_cross.append(chromosome)
            else:
                chromosome_not_to_cross.append(chromosome)

    @staticmethod
    def generate_couples(chromosome_to_cross, chromosome_not_to_cross):
        crossover_tuples = []
        while chromosome_to_cross:
            # Select the first chromosome as the father
            father_chr = chromosome_to_cross.pop()

            # If there is no other chromosome in the list to cross, then append the current father chromosome
            # to the list of chromosomes not to be crossed
            if not chromosome_to_cross:
                chromosome_not_to_cross.append(father_chr)
                break

            mother_chr_index = random.choice(range(len(chromosome_to_cross)))
            mother_chr = chromosome_to_cross[mother_chr_index]
            
            # Remove the selected mother chromosome from the list
            if mother_chr_index is not None:
                del chromosome_to_cross[mother_chr_index]
            
            # Add the pair of chromosomes to the crossover tuples
            crossover_tuples.append((father_chr, mother_chr))
        
        return crossover_tuples

    @staticmethod
    def cross_couples(crossover_couples):
        new_population = []
        for couple in crossover_couples:
            # Perform crossover on each couple and generate two children
            child1, child2 = Crossover2X.cross_chromosomes(couple, random.randint(0, len(couple[0]) - 1),
                                                           random.randint(0, len(couple[0]) - 1))
            
            # Add the children to the new population
            new_population.append(child1)
            new_population.append(child2)
        
        return new_population

    @staticmethod
    def cross_chromosomes(couple, point1: int, point2: int):
        if point1 > point2:
            point1, point2 = point2, point1

        father, mother = couple

        # Initialize the children
        child1 = father
        child2 = mother

        # Extract the central part of each chromosome
        f_swap = father[point1:point2]
        m_swap = mother[point1:point2]

        # Swap the central part
        child1[point1:point2] = m_swap
        child2[point1:point2] = f_swap

        return child1, child2

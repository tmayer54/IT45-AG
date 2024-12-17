import numpy as np


def compute_fitness_second(population, mission_list, employee_list, pop_distances):
    """
    Compute the fitness for the assignment of employees to missions (second population).

    Args:
        population (list): List of chromosomes representing employee assignments.
        mission_list (list): List of missions.
        employee_list (list): List of employees.
        pop_distances (list): List of distances for each chromosome.

    Returns:
        fitness_list (list): List of fitness values for each chromosome.
    """
    fitness_list = []

    # For each chromosome in the population
    i = 0
    for chromosome in population:
        fitness_sum = 0
        for index, x in enumerate(chromosome):
            if x > 0:
                # Add a fitness value based on specialty match between mission and employee
                fitness_sum += 1000000000 + 1000000 * int(mission_list[index].specialty == employee_list[int(x - 1)].specialty)

        # Add a fitness value based on the negative distance traveled
        fitness_sum += 1000000 - pop_distances[i]
        i += 1

        fitness_list.append(fitness_sum)

    return fitness_list


def compute_fitness_first(population, distance_matrix):
    """
    Compute the fitness for the assignment of missions to centers (first population).

    Args:
        population (list): List of chromosomes representing mission assignments.
        distance_matrix (numpy.ndarray): Matrix of distances between missions and centers.

    Returns:
        fitness_list (list): List of fitness values for each chromosome.
    """
    fitness_list = []

    for chromosome in population:
        index = 0
        fitness_sum = 0
        for x in chromosome:
            fitness_sum += distance_matrix[int(x) - 1][index]
            index += 1

        fitness_list.append(fitness_sum)

    return fitness_list


def normalize_fitness(fitness_list):
    """
    Normalize the fitness values to sum up to 1.

    Args:
        fitness_list (list): List of fitness values.

    Returns:
        normalized_fitness (numpy.ndarray): Normalized fitness values.
    """
    sum_fitness = np.sum(fitness_list)
    if sum_fitness != 0:
        normalized_fitness = np.array(fitness_list) / sum_fitness
    else:
        normalized_fitness = np.zeros_like(fitness_list)

    return normalized_fitness
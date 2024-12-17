import numpy as np
import time

import utilz.generate_population as gp
from config import POPULATION_SIZE, NUMBER_OF_GENERATIONS, PATH_DISTANCES, PATH_CENTERS, PATH_MISSIONS, \
    PATH_EMPLOYEES
from utilz.crossover import Crossover, Crossover2X
from utilz.fitness import compute_fitness_first, compute_fitness_second, normalize_fitness
from utilz.getData import read_distance_csv, read_employees_csv, read_missions_csv, get_centers_number
from utilz.mutation import Mutation, MutationSwitch
from utilz.selection import Selection, RouletteSelection

# Initialize the selection, mutation, and crossover strategies
selection_strategy = Selection(selection_algorithm=RouletteSelection())
mutation_strategy = Mutation(mutation_algorithm=MutationSwitch())
crossover_strategy = Crossover(crossover_algorithm=Crossover2X())

# Read the distance matrix, employee list, mission list, and number of centers from CSV files
distance_matrix = read_distance_csv(PATH_DISTANCES)
employee_list = read_employees_csv(PATH_EMPLOYEES)
mission_list = read_missions_csv(PATH_MISSIONS)
number_of_centers = get_centers_number(PATH_CENTERS)

def main():
    # Initialize variables for tracking results
    generation_indices = []
    avg_result = []
    max_result = []
    min_result = []

    # Initialize an array to store the number of employees per center
    number_of_employee_per_center = np.zeros(number_of_centers + 1, dtype=int)

    # Calculate the number of employees per center
    for emp in employee_list:
        number_of_employee_per_center[emp.center_id] += 1

    # Calculate the cumulative sum of the number of employees per center
    cumulative_sum_of_employee = np.cumsum(number_of_employee_per_center)

    # Generate the initial random population
    population = gp.generate_random_population(len(mission_list), number_of_centers, POPULATION_SIZE)

    # Compute the fitness of the initial population
    first_fitness = compute_fitness_first(population, distance_matrix)
    first_normalized_fitness = normalize_fitness(first_fitness)

    # Iterate over the number of generations
    for iter_first in range(NUMBER_OF_GENERATIONS):
        # Generate the second population based on the assignment of employees to missions
        result = gp.generate_second_population(population, cumulative_sum_of_employee, POPULATION_SIZE,
                                               employee_list, distance_matrix, mission_list, number_of_centers)
        assignment_pop = result[0]
        pop_distances = result[1]

        for iter_second in range(NUMBER_OF_GENERATIONS):
            # Initialize variables for tracking fitness values
            max_fitness = 0.0
            min_fitness = 0.0
            avg_fitness = 0.0

            # Compute the fitness of the second population
            fitness = compute_fitness_second(assignment_pop, mission_list, employee_list, pop_distances)
            normalized_fitness = normalize_fitness(fitness)

            # Update the maximum, minimum, and average fitness values
            max_fitness = np.max(fitness)
            min_fitness = np.min(fitness)
            avg_fitness += np.mean(fitness)

            if len(assignment_pop) > 0:
                avg_fitness /= len(assignment_pop)

            # Update the result tracking lists
            max_result.append(max_fitness)
            min_result.append(min_fitness)
            avg_result.append(avg_fitness)
            generation_indices.append(iter_first * NUMBER_OF_GENERATIONS + iter_second)

            # Determine the maximum fitness chromosome
            max_chromosome = assignment_pop[np.argmax(fitness)] if len(fitness) > 0 and len(assignment_pop) > 0 else None

            # Perform selection, crossover, and mutation operations on the second population
            selected_2pop = selection_strategy.select(assignment_pop, normalized_fitness)
            crossed_2pop = crossover_strategy.crossover(selected_2pop)
            mutated_2pop = mutation_strategy.mutate(crossed_2pop)

            print("iter", iter_first * NUMBER_OF_GENERATIONS + iter_second, "  /  ", max_fitness)

            # Update the second population with the mutated individuals
            assignment_pop = mutated_2pop

        # Perform selection, crossover, and mutation operations on the first population
        selected_1pop = selection_strategy.select(population, first_normalized_fitness)
        crossed_1pop = crossover_strategy.crossover(selected_1pop)
        mutated_1pop = mutation_strategy.mutate(crossed_1pop)

        # Update the first population with the mutated individuals
        population = mutated_1pop

    # Print the maximum fitness value achieved
    print("Max fitness:", np.max(max_result))


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
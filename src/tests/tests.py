import random

import numpy as np

from src.utilz import generate_population
from src.utilz.crossover import Crossover, Crossover2X
from src.utilz.fitness import compute_fitness_first, compute_fitness_second
from src.utilz.generate_population import generate_second_population
from src.utilz.getData import read_distance_csv, read_missions_csv, read_employees_csv
from src.utilz.mutation import Mutation, MutationSwitch
from src.utilz.selection import Selection, RouletteSelection

print("################################## Imports ########################################")
print()
print("Distance matrix:")
dist = read_distance_csv('../../instances/94Missions-2centres/distances.csv')
print(dist)
print("Employees:")
emp = read_employees_csv('../../instances/94Missions-2centres/employees.csv')
for employee in emp:
    employee.display_info()

number_of_employee_per_center = np.zeros(3)
for e in emp:
    number_of_employee_per_center[e.center_id] += 1
print("number employee per center:", number_of_employee_per_center)
cumulative_sum_of_employee = np.cumsum(number_of_employee_per_center)
print("Cumulative sum:", cumulative_sum_of_employee)
print("Missions:")
miss = read_missions_csv('../../instances/94Missions-2centres/missions.csv')
for missions in miss:
    missions.display_info()

print()
print("################################## Generation ########################################")
print()
pop = generate_population.generate_random_population(94, 2, 7)
fitness_list = list(range(len(pop)))
random.shuffle(fitness_list)
print("Generated population :", pop)
print()
selector = Selection(selection_algorithm=RouletteSelection())
selected_pop = selector.select(pop, fitness_list)
print("Selected population :", selected_pop)
print()
crossover = Crossover(crossover_algorithm=Crossover2X())
cross_pop = crossover.crossover(selected_pop)
print("Crossed population :", cross_pop)
print()
mutator = Mutation(mutation_algorithm=MutationSwitch())
mut_pop = mutator.mutate(cross_pop)
print("Mutated population :", mut_pop)
fitness_list = compute_fitness_first(mut_pop, distance_matrix=dist)
print()
print("Fitness : ", fitness_list)

sec_pop = generate_second_population(mut_pop, 94, cumulative_sum_of_employee, 7)
fitness2_list = compute_fitness_second(sec_pop, fitness_list, mission_list=miss,
                                       employee_list=emp)
print("fitness2: ", fitness2_list)

import random
import time
from config import ASSIGNATION_PROBABILITY, MAX_WORKING_HOURS_PER_WEEK, MAX_WORKING_HOURS_PER_DAY, MAX_WORKING_HOURS_PER_DAY_AMPLITUDE
from utilz.getData import read_distance_csv, read_employees_csv, read_missions_csv, get_centers_number, find_mission_by_id

import numpy as np

def generate_random_population(number_of_missions: int, number_of_centers: int, number_of_chromosomes: int):
    """
    Generates a random population representing the assignments of missions to centers.

    Parameters:
    - number_of_missions: The total number of missions.
    - number_of_centers: The total number of centers.
    - number_of_chromosomes: The size of the population (number of individuals).

    Returns:
    - A list representing the random population of assignments.
    """

    # Initialize an empty list to store the population
    population_list = []

    # Set the seed for the random number generator based on the current time
    random.seed(time.localtime())

    # Generate the specified number of individuals (chromosomes) in the population
    for _ in range(number_of_chromosomes):
        # Create a new individual (chromosome) with all zeros
        new_chromosome = np.zeros(number_of_missions)

        # Assign random centers to the missions
        for i in range(number_of_missions):
            # Assign a random center ID between 1 and the total number of centers
            new_chromosome[i] = random.randint(1, number_of_centers)

        # Add the new individual to the population
        population_list.append(new_chromosome)

    # Return the generated population
    return population_list


# Generates a population that correspond to the assignments of the employees to the missions
def generate_second_population(population, number_of_employee, number_of_chromosomes: int, 
                        employee_list, distance_matrix, mission_list, number_of_centers: int):

    """
    Generates a population that corresponds to the assignments of the employees to the missions.

    Parameters:
    - population: A list representing the initial population.
    - number_of_employee: The number of employees.
    - number_of_chromosomes: The number of chromosomes (assignments) in each individual.
    - employee_list: A list of all employees.
    - distance_matrix: A matrix representing the distances between mission locations.
    - mission_list: A list of all available missions.
    - number_of_centers: The number of centers in the distance matrix.

    Returns:
    - A new population with assignments of employees to missions and the total distance traveled for each chromosome.
    """
    second_population_list = []
    travel_speed = 50/60 # Travel speed in km/min
    pop_distance = []
    total_travel_distance = 0
    travel_distance = 0
    random.seed(time.localtime())
    for n in range(number_of_chromosomes):
        new_chromosome = np.zeros(len(mission_list))

        #Reset employee for the new chromosome 
        for emp in employee_list:
            #print(f"Employee {emp.employee_id} assigned to {employee_list[emp.employee_id - 1].missions}missions")
            emp.working_hours = [0,0,0,0,0,0,0]
            emp.workday_begin_time = [0, 0, 0, 0, 0, 0, 0]
            emp.workday_end_time = [0, 0, 0, 0, 0, 0, 0]
            emp.missions = []

        #Assign the missions to the employees by day
        for day in range(1,8):
            mission_of_the_day = []
            #Get the missions of the day
            for d in mission_list:
                if int(d.day) == day:
                    mission_of_the_day.append(d)
            #Assign missions of the day to the employees
            for mission in mission_of_the_day:

                # 0 -> mission not assigned, else mission assigned to the employee id
                if random.uniform(0, 1) < ASSIGNATION_PROBABILITY:
                    id_center = int(population[n][mission.mission_id - 1])
                    available_employees = list(
                        range(int(number_of_employee[id_center - 1]) + 1, int(number_of_employee[id_center]+1))
                    )

                    first_mission = None
                    last_mission = None

                    total_travel_distance += travel_distance
                    travel_distance = 0

                    for employee in available_employees:
                        #Get the time of the mission
                        mission_time = int(mission.ending_period) - int(mission.starting_period)

                        #Calculate the travel time
                        travel_distance = calculate_distance_between_missions(employee_list[employee - 1], mission, distance_matrix, number_of_centers, mission_list, id_center)
                        travel_time = travel_distance / travel_speed
                        
                        if employee_list[employee - 1].missions != []:
                            first_mission = find_mission_by_id(employee_list[employee - 1].missions[0] + 1, mission_list)
                            last_mission = find_mission_by_id(employee_list[employee - 1].missions[-1] + 1, mission_list)
                            for mission_id in employee_list[employee - 1].missions:
                                m = find_mission_by_id(mission_id + 1, mission_list)
                                if m.ending_period > last_mission.ending_period:
                                    last_mission = m
                                elif m.starting_period < first_mission.starting_period:
                                    first_mission = m

                        # Update the workday begin and end time
                        if first_mission == None:
                            updated_begin_time = int(mission.starting_period)
                        else:
                            updated_begin_time = int(mission.starting_period) if int(mission.starting_period) < int(first_mission.starting_period) else first_mission.starting_period
                        if last_mission == None:
                            updated_end_time = int(mission.ending_period)
                        else:
                            updated_end_time = int(mission.ending_period) if int(mission.ending_period) > int(last_mission.ending_period) else last_mission.ending_period
                        
                        if constraint_verif(employee_list[employee - 1],day,employee_list[employee - 1].workday_begin_time[day],
                            employee_list[employee - 1].workday_end_time[day],mission_time,travel_time) == True and check_mission_overlap(employee_list[employee - 1],mission,distance_matrix,travel_speed,number_of_centers, mission_list
                        ) == False:
                            #Update the employee
                            employee_list[employee - 1].working_hours[day] = mission_time
                            employee_list[employee - 1].workday_begin_time[day] = updated_begin_time
                            employee_list[employee - 1].workday_end_time[day] = updated_end_time
                            employee_list[employee - 1].missions.append(mission.mission_id - 1)
                            #Update the chromosome
                            new_chromosome[mission.mission_id - 1] = employee
                            break
                            
                else:
                    new_chromosome[mission.mission_id - 1] = 0
        #Add the chromosome to the population
        second_population_list.append(new_chromosome)
        pop_distance.append(total_travel_distance)

    return second_population_list, pop_distance

def constraint_verif(employee, day, start_time, end_time, mission_time, travel_time):
    """
    Checks if a mission can be assigned according to the constraints.

    Args:
        employee (Employee): The employee object.
        day (int): The day of the week.
        start_time (int): The starting time of the mission.
        end_time (int): The ending time of the mission.
        mission_time (int): The duration of the mission.
        travel_time (float): The travel time from the previous mission.

    Returns:
        bool: True if the mission can be assigned, False otherwise.
    """

    if (
        employee.working_hours[day] + mission_time + travel_time <= MAX_WORKING_HOURS_PER_DAY
        and np.sum(employee.working_hours) + mission_time + travel_time <= MAX_WORKING_HOURS_PER_WEEK
        and int(end_time) - int(start_time) <= MAX_WORKING_HOURS_PER_DAY_AMPLITUDE
    ):
        return True
    else:
        return False
    

def check_mission_overlap(employee, mission, distance_matrix, travel_speed, number_of_centers, mission_list):
    """
    Check if there is an overlap between a given mission and an employee's existing missions.

    Parameters:
    - employee: An object representing an employee.
    - mission: An object representing the mission to be checked for overlap.
    - distance_matrix: A matrix representing the distances between mission locations.
    - travel_speed: The speed at which the employee travels between mission locations.
    - number_of_centers: The number of centers in the distance matrix.
    - mission_list: A list of all available missions.

    Returns:
    - True if there is an overlap with existing missions, False otherwise.
    """

    prev_mission = None
    next_mission = None

    # Check for overlapping missions with previous and next missions
    for mission_id in employee.missions:
        m = find_mission_by_id(mission_id + 1, mission_list)

        if m.ending_period < mission.starting_period:
            if prev_mission is None or m.ending_period > prev_mission.ending_period:
                prev_mission = m
        elif m.starting_period > mission.ending_period:
            if next_mission is None or m.starting_period < next_mission.starting_period:
                next_mission = m

    # Calculate travel time to the previous mission
    if prev_mission is not None:
        travel_distance_prev = distance_matrix[
            prev_mission.mission_id - 1 + number_of_centers, mission.mission_id - 1 + number_of_centers
        ]
        travel_time_prev = travel_distance_prev / travel_speed
        if float(prev_mission.ending_period) > float(mission.starting_period) - float(travel_time_prev):
            return True  # Overlapping missions found

    # Calculate travel time to the next mission
    if next_mission is not None:
        travel_distance_next = distance_matrix[
            mission.mission_id - 1 + number_of_centers, next_mission.mission_id - 1 + number_of_centers
        ]
        travel_time_next = travel_distance_next / travel_speed
        if float(mission.ending_period) > float(next_mission.starting_period) - float(travel_time_next):
            return True  # Overlapping missions found

    return False  # No overlap with existing missions


def calculate_distance_between_missions(employee, next_mission, distance_matrix, number_of_centers, mission_list, center_id):
    """
    Calculate the total distance between an employee's existing missions and the next mission to be assigned.

    Parameters:
    - employee: An object representing an employee.
    - next_mission: An object representing the next mission to be assigned.
    - distance_matrix: A matrix representing the distances between mission locations.
    - number_of_centers: The number of centers in the distance matrix.
    - mission_list: A list of all available missions.
    - center_id: The ID of the center where the employee is located.

    Returns:
    - The total distance in traveling from the employee's existing missions to the next mission.
    """

    mission = []
    for mission_id in employee.missions:
        mission.append(find_mission_by_id(mission_id + 1, mission_list))
    
    mission.append(next_mission)

    # Sort missions by starting period
    mission = sort_missions_by_starting_period(mission)

    total_distance = 0
    for i in range(len(mission) - 1):
        total_distance += distance_matrix[
            mission[i].mission_id - 1 + number_of_centers, mission[i + 1].mission_id - 1 + number_of_centers
        ]

    # Add distance from the center to the first mission
    total_distance += distance_matrix[center_id - 1, mission[0].mission_id - 1 + number_of_centers]
    return total_distance


def sort_missions_by_starting_period(missions):
    """
    Sort a list of missions based on their starting periods in ascending order.

    Parameters:
    - missions: A list of mission objects.

    Returns:
    - A sorted list of missions based on their starting periods.
    """
    sorted_missions = sorted(missions, key=lambda mission: mission.starting_period)
    return sorted_missions
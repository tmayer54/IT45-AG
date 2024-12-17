import csv
import numpy as np
from object.employee import Employees
from object.mission import Missions
from object.skill import Skill
from object.specialty import Specialty

def assign_skill_enum(skill_string):
    """
    Assigns the Skill enum based on the skill string.

    Args:
        skill_string (str): Skill string.

    Returns:
        skill_enum (Skill): Skill enum value.
    """
    if skill_string == "LSF":
        skill_enum = Skill.LSF
    elif skill_string == "LPC":
        skill_enum = Skill.LPC
    else:
        skill_enum = Skill.OTHER

    return skill_enum


def assign_specialty_enum(specialty_string):
    """
    Assigns the Specialty enum based on the specialty string.

    Args:
        specialty_string (str): Specialty string.

    Returns:
        specialty_enum (Specialty): Specialty enum value.
    """
    if specialty_string == "Electricite":
        specialty_enum = Specialty.Electricite
    elif specialty_string == "Mecanique":
        specialty_enum = Specialty.Mecanique
    elif specialty_string == "Musique":
        specialty_enum = Specialty.Musique
    elif specialty_string == "Jardinage":
        specialty_enum = Specialty.Jardinage
    elif specialty_string == "Menuiserie":
        specialty_enum = Specialty.Menuiserie
    else:
        specialty_enum = Specialty.OTHER

    return specialty_enum


def read_distance_csv(file_path):
    """
    Read a CSV file containing distance data and return it as a NumPy array.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        distances_array (numpy.ndarray): Array containing distance data.
    """
    distances = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            distances.append(row)

    # Convert the list of lists to a NumPy array
    distances_array = np.array(distances, dtype=np.float32)

    return distances_array


def read_missions_csv(file_path):
    """
    Read a CSV file containing mission data and return a list of Missions objects.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        missions (list): List of Missions objects.
    """
    missions = []

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            mission_id = int(row[0])
            day = row[1]
            starting_period = row[2]
            ending_period = row[3]
            skill = assign_skill_enum(row[4])
            specialty = assign_specialty_enum(row[5])

            mission = Missions(mission_id, day, starting_period, ending_period, skill, specialty)
            missions.append(mission)

    return missions


def read_employees_csv(file_path):
    """
    Read a CSV file containing employee data and return a list of Employees objects.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        employees (list): List of Employees objects.
    """
    employees = []

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            employee_id = int(row[0])
            center_id = int(row[1])
            skill = assign_skill_enum(row[2])
            specialty = assign_specialty_enum(row[3])

            employee = Employees(employee_id, center_id, skill, specialty)
            employees.append(employee)

    return employees


def get_centers_number(file_path):
    """
    Get the number of centers from the CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        centers_number (int): Number of centers.
    """
    return sum(1 for _ in open(file_path))


def find_mission_by_id(mission_id, mission_list):
    """
    Find a mission by its ID in the mission list.

    Args:
        mission_id (int): ID of the mission.
        mission_list (list): List of missions.

    Returns:
        mission (Missions): Mission object if found, None otherwise.
    """
    for mission in mission_list:
        if mission.mission_id == mission_id:
            return mission

    return None
class Employees:
    def __init__(self, employee_id, center_id, skill, specialty):
        """
        Initializes an instance of the Employees class.

        Args:
        - employee_id (int): The ID of the employee.
        - center_id (int): The ID of the center where the employee works.
        - skill (str): The skill of the employee.
        - specialty (str): The specialty of the employee.
        """
        self.employee_id = employee_id
        self.center_id = center_id
        self.skill = skill
        self.specialty = specialty
        self.working_hours = [0, 0, 0, 0, 0, 0, 0]  # Total working hours for each day of the week
        self.workday_begin_time = [0, 0, 0, 0, 0, 0, 0]  # Time at which the workday begins for each day of the week
        self.workday_end_time = [0, 0, 0, 0, 0, 0, 0]  # End time of the workday for each day of the week
        self.missions = []  # List of missions assigned to the employee

    def display_info(self):
        """
        Displays the information of the employee.
        """
        print(f"Employee ID: {self.employee_id}")
        print(f"Center ID: {self.center_id}")
        print(f"Skill: {self.skill}")
        print(f"Specialty: {self.specialty}")
        print(f"Working Hours: {self.working_hours}")
        print(f"Workday Begin Time: {self.workday_begin_time}")
        print(f"Workday End Time: {self.workday_end_time}")
        print(f"Missions: {self.missions}")
        print("------------------------------------------")

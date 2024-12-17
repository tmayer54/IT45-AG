class Missions:
    def __init__(self, mission_id, day, starting_period, ending_period, skill, specialty):
        """
        Initializes an instance of the Missions class.

        Args:
        - mission_id (int): The ID of the mission.
        - day (int): The day of the mission.
        - starting_period (int): The starting period of the mission.
        - ending_period (int): The ending period of the mission.
        - skill (str): The required skill for the mission.
        - specialty (str): The required specialty for the mission.
        """
        self.mission_id = mission_id
        self.day = day
        self.starting_period = starting_period
        self.ending_period = ending_period
        self.skill = skill
        self.specialty = specialty
    
    def display_info(self):
        """
        Displays the information of the mission.
        """
        print(f"Mission ID: {self.mission_id}")
        print(f"Day: {self.day}")
        print(f"Starting Period: {self.starting_period}")
        print(f"Ending Period: {self.ending_period}")
        print(f"Skill: {self.skill}")
        print(f"Specialty: {self.specialty}")
        print("------------------------------------------")

    def getID(self):
        """
        Returns the ID of the mission.
        """
        return self.mission_id
    
    def printID(self):
        """
        Prints the ID of the mission.
        """
        print(f"Mission ID: {self.mission_id}")

# File verified

# Importing necessary libraries
import sys
import os

# Get the absolute path of the parent directory by navigating one level up from the current file's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Append the parent directory to the Python system path
sys.path.append(parent_dir)

# Import the Person class from the utilities module
try:
    from classes.person import Person
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'Person' class could not be found. Ensure the correct path and file exist.")

# Class representing a secretary
class Secretary(Person):
    def __init__(self, last_name, first_name, email):
        """
        Constructor for the Secretary class.

        :param last_name: Last name of the secretary.
        :param first_name: First name of the secretary.
        :param email: Email of the secretary.
        """
        super().__init__(last_name, first_name, email)
        self._role = 'secretary'
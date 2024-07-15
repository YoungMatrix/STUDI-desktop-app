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

# Class representing a patient
class Patient(Person):
    def __init__(self, id, last_name, first_name, address, email, history=None, prescription=None):
        """
        Constructor for the Patient class.

        :param id: Identifier of the patient.
        :param last_name: Last name of the patient.
        :param first_name: First name of the patient.
        :param address: Address of the patient.
        :param email: Email of the patient.
        :param history: History object associated with the patient. Defaults to None.
        :param prescription: Prescription object associated with the patient. Defaults to None.
        """
        super().__init__(last_name, first_name, email)
        self._role = 'patient'
        self._id = id
        self._address = address
        self._history = history
        self._prescription = prescription

    # Getter for id property
    @property
    def id(self):
        """
        Getter method for accessing the id property.

        :return: The id of the patient (str).
        """
        return self._id
    
    # Getter for address property
    @property
    def address(self):
        """
        Getter method for accessing the address property.

        :return: The address of the patient (str).
        """
        return self._address

    # Getter for history property
    @property
    def history(self):
        """
        Getter method for accessing the history property.

        :return: The history object associated with the patient.
        """
        return self._history

    # Getter for prescription property
    @property
    def prescription(self):
        """
        Getter method for accessing the prescription property.

        :return: The prescription object associated with the patient.
        """
        return self._prescription

    # Methods to add history and prescription
    def add_history(self, history):
        """
        Adds a history entry to the patient's history.

        :param history: A History object.
        """
        self._history = history

    def add_prescription(self, prescription):
        """
        Adds a prescription entry to the patient's prescription.

        :param prescription: A Prescription object.
        """
        self._prescription = prescription

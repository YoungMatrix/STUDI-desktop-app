# File verified

# Importing necessary libraries
from datetime import date

# Class to store prescription details
class Prescription:
    def __init__(self, id, label, prescription_date, start_date, end_date, description, medication_details):
        """
        Initializes a new instance of the Prescription class.

        :param id: The id of the prescription (str).
        :param label: The label of the prescription (str).
        :param prescription_date: The date of the prescription (str).
        :param start_date: The start date of the prescription (str).
        :param end_date: The end date of the prescription (str).
        :param description: The description of the prescription (str).
        :param medication_details: The list of medications with their dosages (list of dicts).
        """
        self._id = id
        self._label = label
        self._prescription_date = prescription_date
        self._start_date = start_date
        self._end_date = end_date
        self._description = description
        self._medication_details = medication_details

    # Getter for id property
    @property
    def id(self):
        """
        Returns the id of the prescription.

        :return: The id (str).
        """
        return self._id
    
    # Getter for label property
    @property
    def label(self):
        """
        Returns the label of the prescription.

        :return: The label (str).
        """
        return self._label

    # Getter for prescription_date property
    @property
    def prescription_date(self):
        """
        Returns the prescription date in dd/mm/yyyy format.

        :return: The prescription date (str).
        """
        return self._convert_date(self._prescription_date)

    # Getter for start_date property
    @property
    def start_date(self):
        """
        Returns the start date in dd/mm/yyyy format.

        :return: The start date (str).
        """
        return self._convert_date(self._start_date)

    # Getter for end_date property
    @property
    def end_date(self):
        """
        Returns the end date in dd/mm/yyyy format.

        :return: The end date (str).
        """
        return self._convert_date(self._end_date)

    # Getter for description property
    @property
    def description(self):
        """
        Returns the description of the prescription.

        :return: The description (str).
        """
        return self._description

    # Getter for medication_details property
    @property
    def medication_details(self):
        """
        Returns the list of medication details.

        :return: The medication details (list of dicts).
        """
        return self._medication_details

    # Static method to convert date format 
    @staticmethod
    def _convert_date(date_obj):
        """
        Converts a date object to dd/mm/yyyy format.

        :param date_obj: The date object (datetime.date).
        :return: The date string in dd/mm/yyyy format (str).
        """
        # Check if the input is a date object
        if isinstance(date_obj, date):
            # Return the date string in the desired format
            return date_obj.strftime("%d/%m/%Y")
        else:
            raise ValueError("Input must be a datetime.date object")
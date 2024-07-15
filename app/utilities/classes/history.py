# File verified

# Importing necessary libraries
from datetime import date

# Class to store history details
class History:
    def __init__(self, id, pattern, field, doctor, entrance_date, release_date):
        """
        Initializes a new instance of the History class.

        :param id: The id of history (str).
        :param pattern: The reason for the history entry (str).
        :param field: The medical specialty (str).
        :param doctor: The name of the doctor (str).
        :param entrance_date: The entry date (str).
        :param release_date: The exit date (str).
        """
        self._id = id
        self._pattern = pattern
        self._field = field
        self._doctor = doctor
        self._entrance_date = entrance_date
        self._release_date = release_date

    # Getter for id property
    @property
    def id(self):
        """
        Returns the id of the history.

        :return: The id (str).
        """
        return self._id

    # Getter for pattern property
    @property
    def pattern(self):
        """
        Returns the reason for the history entry.

        :return: The reason (str).
        """
        return self._pattern

    # Getter for field property
    @property
    def field(self):
        """
        Returns the medical field.

        :return: The field (str).
        """
        return self._field

    # Getter for doctor property
    @property
    def doctor(self):
        """
        Returns the name of the doctor.

        :return: The doctor (str).
        """
        return self._doctor

    # Getter for entrance_date property
    @property
    def entrance_date(self):
        """
        Returns the entry date.

        :return: The entry date (str) in the format dd/mm/yyyy.
        """
        return self._convert_date(self._entrance_date)

    # Getter for release_date property
    @property
    def release_date(self):
        """
        Returns the exit date.

        :return: The exit date (str) in the format dd/mm/yyyy.
        """
        return self._convert_date(self._release_date)

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
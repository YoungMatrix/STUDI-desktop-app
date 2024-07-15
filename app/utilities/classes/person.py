# File verified

# Class representing a person with basic information
class Person:
    def __init__(self, last_name, first_name, email):
        """
        Constructor for the Person class.

        :param last_name: Last name of the person.
        :param first_name: First name of the person.
        :param email: Email of the person.
        """
        self._last_name = last_name
        self._first_name = first_name
        self._email = email
        # Default role is empty for generic Person
        self._role = ''

    # Getter for last_name property
    @property
    def last_name(self):
        """
        Getter for the last name.

        :return: Last name of the person.
        """
        return self._last_name

    # Getter for first_name property
    @property
    def first_name(self):
        """
        Getter for the first name.

        :return: First name of the person.
        """
        return self._first_name

    # Getter for email property
    @property
    def email(self):
        """
        Getter for the email.

        :return: Email of the person.
        """
        return self._email

    # Getter for role property
    @property
    def role(self):
        """
        Getter for the role.

        :return: Role of the person.
        """
        return self._role

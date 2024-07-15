# File verified

# Importing necessary libraries
import sys
import os

# Get the absolute path of the parent directory by navigating one level up from the current file's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Append the parent directory to the Python system path
sys.path.append(parent_dir)

# Import the function 'retrieve_secretary' from secretary_model
try:
    from model.secretary_model import retrieve_secretary
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'retrieve_secretary' function could not be found. Ensure the correct path and file exist.")

# Function to check if secretary retrieval was successful
def success_secretary_retrieval(email, entered_password):
    """
    Function to check if secretary retrieval was successful.

    :param email: The email of the secretary.
    :param entered_password: The password entered by the secretary.
    :return: Secretary object if retrieval is successful, otherwise None.
    """
    # Retrieve the secretary using the provided email and password
    secretary = retrieve_secretary(email, entered_password)

    # Check if the retrieval was successful
    if secretary is not None:
        return secretary
    else:
        return None

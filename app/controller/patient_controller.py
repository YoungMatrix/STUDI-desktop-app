# File verified

# Importing necessary libraries
import sys
import os

# Get the absolute path of the parent directory by navigating one level up from the current file's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Append the parent directory to the Python system path
sys.path.append(parent_dir)

# Import the functions 'retrieve_patient' and 'retrieve_information_patient' from patient_model
try:
    from model.patient_model import retrieve_patient, retrieve_information_patient
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'retrieve_patient' and 'retrieve_information_patient' functions could not be found. Ensure the correct path and file exist.")

# Function to check if patient list retrieval was successful
def success_patient_list_retrieval(date):
    """
    Function to check if patient retrieval was successful.

    :param date: The date for which to retrieve patients.
    :return: List of patients if retrieval is successful, otherwise an empty list.
    """
    # Format the datetime object as a string in the desired format
    formatted_date = date.strftime("%Y-%m-%d")

    # Retrieve the list of patients using the provided date
    patientList = retrieve_patient(formatted_date)
    
    return patientList

# Function to check if patient information retrieval was successful
def success_information_patient_retrieval(patient, date):
    """
    Function to check if patient information retrieval was successful.

    :param patient: The patient instance to update with retrieved information.
    :param date: The date for which to retrieve patient information.
    :return: Updated patient instance if retrieval is successful, otherwise the original patient instance.
    """
    # Format the datetime object as a string in the desired format
    formatted_date = date.strftime("%Y-%m-%d")
    
    # Call the function to retrieve patient information for the given date
    updated_patient = retrieve_information_patient(patient, formatted_date)

    # Return the updated patient instance
    return updated_patient
# File verified

# Import necessary libraries
from datetime import datetime
import sys
import os

# Get the absolute path of the parent directory by navigating one level up from the current file's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Append the parent directory to the Python system path
sys.path.append(parent_dir)

# Import the 'execute_query_from_file' function from database.py
try:
    from utilities.functions.database import execute_query_from_file
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'execute_query_from_file' function could not be found. Ensure the correct path and file exist.")

# Import the configuration settings
try:
    from configuration import config
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'config' file could not be found. Ensure the correct path and file exist.")

# Import the Database class from the utilities module
try:
    from utilities.classes.database import Database
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'Database' class could not be found. Ensure the correct path and file exist.")

# Import the Patient class from the utilities module
try:
    from utilities.classes.patient import Patient
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'Patient' class could not be found. Ensure the correct path and file exist.")

# Import the History class from the utilities module
try:
    from utilities.classes.history import History
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'History' class could not be found. Ensure the correct path and file exist.")

# Import the Prescription class from the utilities module
try:
    from utilities.classes.prescription import Prescription
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'Prescription' class could not be found. Ensure the correct path and file exist.")

# Function to retrieve patients from the database based on the given date
def retrieve_patient(date):
    """
    Function to retrieve patients from the database based on the given date.
    
    :param date: The date to filter patients.
    :return: List of Patient instances if retrieval is successful, empty list if not.
    """
    # Create a Database instance with the given configuration
    db = Database(
        host=config.DB_HOST, 
        user=config.DB_USER, 
        password=config.DB_PASSWORD, 
        database=config.DB_DATABASE, 
        port=config.DB_PORT 
    )

    try:
        # Connect to the database
        if not db.connect():
            return None

        # Execute the query to get patients by date
        result = execute_query_from_file(db, "app/assets/sql/get_patients_by_date.sql", (date,))

        if result:
            patient_list = []
            # Iterate through the results and create Patient instances
            for record in result:
                patient = Patient(
                    id=record[0], 
                    last_name=record[1], 
                    first_name=record[2], 
                    address=record[3],
                    email=record[4]
                )
                patient_list.append(patient)
            return patient_list

        # Return an empty list if no patient is found
        return []

    except Exception as e:
        # Print the exception message if there is a network or connection error
        print(f"Network or connection error: {e}")
        return []

    finally:
        # Disconnect from the database
        db.disconnect()

# Function to retrieve patient's history from the database based on the given date.
def retrieve_information_patient(patient, date):
    """
    Function to retrieve patient's history from the database based on the given date.
    
    :param patient: The patient instance to update with the retrieved information.
    :param date: The date to filter patient's history.
    :return: Updated Patient instance if retrieval is successful, the same Patient instance if not.
    """
    # Create a Database instance with the given configuration
    db = Database(
        host=config.DB_HOST, 
        user=config.DB_USER, 
        password=config.DB_PASSWORD, 
        database=config.DB_DATABASE, 
        port=config.DB_PORT 
    )

    try:
        # Connect to the database
        if not db.connect():
            # If connection fails, return None
            return None

        # Execute the SQL query to retrieve patient history by patient ID and date
        result = execute_query_from_file(db, "app/assets/sql/get_patient_history_by_id_patient_and_date.sql", (patient.id, date,))

        if result:
            # Extract the data from the query result
            id_history = result[0][0]
            id_prescription = result[0][1]
            name_pattern = result[0][2]
            name_field = result[0][3]
            last_name_doctor = result[0][4]
            entrance_date = result[0][5]
            release_date = result[0][6]

            # Check if entrance_date is not already a date object
            if not hasattr(entrance_date, 'year'):
                # Convert entrance_date to datetime.date
                entrance_date = datetime.strptime(entrance_date, "%Y-%m-%d").date()

            # Check if release_date is not already a date object
            if not hasattr(release_date, 'year'):
                # Convert release_date to datetime.date
                release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
            
            # Create a History instance with the extracted data
            history = History(
                id=id_history,
                pattern=name_pattern,
                field=name_field,
                doctor=last_name_doctor,
                entrance_date=entrance_date,
                release_date=release_date
            )

            # Add the history instance to the patient's history
            patient.add_history(history)

            # Execute query to get patient prescription details by ID
            result = execute_query_from_file(db, "app/assets/sql/get_patient_prescription_by_id_prescription.sql", (id_prescription,))

            if result: 
                # Extract the data from the first row of result
                title_label = result[0][0]
                prescription_date = result[0][1]
                start_date = result[0][2]
                end_date = result[0][3]
                description = result[0][4]

                # Check if prescription_date is not already a date object
                if not hasattr(prescription_date, 'year'):
                    # Convert prescription_date to datetime.date
                    prescription_date = datetime.strptime(prescription_date, "%Y-%m-%d").date()

                # Check if start_date is not already a date object
                if not hasattr(start_date, 'year'):
                    # Convert start_date to datetime.date
                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

                # Check if end_date is not already a date object
                if not hasattr(end_date, 'year'):
                    # Convert end_date to datetime.date
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

                # Initialize medication list
                medication_list = []

                # Iterate through the query result
                for row in result:
                    id_medication = row[5]
                    name_drug = row[6]
                    quantity_dosage = row[7]
                    
                    # Add medication details to list
                    medication_list.append([id_medication, name_drug, quantity_dosage])

                # Create a Prescription instance with the extracted data
                prescription = Prescription(
                    id=id_prescription,
                    label=title_label,
                    prescription_date=prescription_date,
                    start_date=start_date,
                    end_date=end_date,
                    description=description,
                    medication_details=medication_list,
                )

                # Add the prescription instance to the patient's prescription
                patient.add_prescription(prescription)

        # Return the (updated) patient instance
        return patient

    except Exception as e:
        # Print the exception message if there is a network or connection error
        print(f"Network or connection error: {e}")
        # Return the patient instance without modifications in case of an error
        return patient

    finally:
        # Disconnect from the database
        db.disconnect()
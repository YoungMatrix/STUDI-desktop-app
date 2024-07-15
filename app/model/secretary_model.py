# File verified

# Importing necessary libraries
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

# Import the functions from password.py
try:
    from utilities.functions.password import *
except ModuleNotFoundError:
    raise ModuleNotFoundError("The functions could not be found. Ensure the correct path and file exist.")

# Import the Database class from the utilities module
try:
    from utilities.classes.database import Database
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'Database' class could not be found. Ensure the correct path and file exist.")

# Import the Secretary class from the utilities module
try:
    from utilities.classes.secretary import Secretary
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'Secretary' class could not be found. Ensure the correct path and file exist.")

# Function to retrieve a secretary from the database based on the email then create a secretary instance else False or None
def retrieve_secretary(email, entered_password):
    """
    Function to retrieve a secretary from the database based on the email and verify the entered password.
    
    :param email: Email of the secretary.
    :param entered_password: Password entered by the user.
    :return: Secretary instance if retrieval and verification are successful, None if not, False on connection error.
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
            return False

        # Execute the query to get the password by email
        result = execute_query_from_file(db, "app/assets/sql/get_secretary_password_by_email.sql", (email,))

        if result:
            # Hash the entered password
            entered_hashed_password = hash_password(entered_password)
            # Verify the hashed password with the stored password
            success_secretary = verify_password(entered_hashed_password, result[0][0], result[0][1])

            if success_secretary:
                # Execute the query to get the secretary information by email
                result = execute_query_from_file(db, "app/assets/sql/get_secretary_information_by_email.sql", (email,))

                if result:
                    # Return a secretary instance
                    secretary = Secretary(result[0][0], result[0][1], email)
                    return secretary

        # Return None if the secretary is not found or password verification fails
        return None

    except Exception as e:
        # Print the exception message if there is a network or connection error
        print(f"Network or connection error: {e}")
        return False

    finally:
        # Disconnect from the database
        db.disconnect()
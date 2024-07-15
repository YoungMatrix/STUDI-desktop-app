# Import necessary libraries
import sys
import os
import hashlib

# Get the absolute path of the parent directory by navigating two levels up from the current file's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Append the parent directory to the Python system path
sys.path.append(parent_dir)

# Import the configuration settings
try:
    from configuration import config
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'config' file could not be found. Ensure the correct path and file exist.")

# Function to hash the password using SHA-256 algorithm
def hash_password(entered_password):
    """
    Function to hash the password using SHA-256 algorithm.

    :param entered_password: The password to be hashed.
    :return: The hashed password.
    """
    # Hash the entered password using SHA-256 algorithm and return the hashed value
    entered_hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()

    return entered_hashed_password

# Function to verify the entered password against the stored hashed password
def verify_password(entered_hashed_password, hashed_password, hashed_salt):
    """
    Function to verify the entered password against the stored hashed password.

    :param entered_hashed_password: The hashed password entered by the user.
    :param hashed_password: The hashed password stored in the database.
    :param hashed_salt: The hashed salt stored in the database.
    :return: True if the entered password matches the stored hashed password, False otherwise.
    """
    # Hash the secret pepper from the configuration
    hashed_pepper = hashlib.sha256(config.PEPPER.encode()).hexdigest()
    
    # Remove the salt from the stored hashed password
    password_no_salt = hashed_password.replace(hashed_salt, '')
    
    # Remove the pepper from the hashed password without salt
    password_no_salt_no_pepper = password_no_salt.replace(hashed_pepper, '')

    # Check if the entered hashed password matches the hashed password without salt and pepper
    return entered_hashed_password == password_no_salt_no_pepper

# File verified

# Importing necessary libraries
import os

# Import the load_dotenv function from the dotenv module
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the database connection parameters in environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = int(os.getenv("DB_PORT"))

# Font name for text display
FONT_NAME = "Arial"

# Retrieve the pepper used for hashing passwords in environment variables
PEPPER = os.getenv("PEPPER")
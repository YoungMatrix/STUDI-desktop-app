# Setup Instructions

## Prerequisites
- Python 3 should be installed on your system.
- Make sure to add Python 3 to your PATH environment variable.
- Install the MySQL Connector Python library using pip:
    - `pip3 install mysql-connector-python`
- Install the Python dotenv library using pip:
    - `pip3 install python-dotenv`

## Configuration
- Set the following environment variables in a `.env` file in the root directory of your project:
    - `DB_HOST`: The hostname of your MySQL database.
    - `DB_USER`: The username for connecting to the MySQL database.
    - `DB_PASSWORD`: The password for the MySQL user.
    - `DB_DATABASE`: The name of the MySQL database.
    - `DB_PORT`: The port number on which MySQL is running.

## Development Setup
- Make sure to select the correct Python interpreter in your IDE (e.g., Visual Studio Code).
- Ensure that the environment variables mentioned above are set correctly in your `.env` file.

## Usage
- Use the provided classes and functions to interact with your MySQL database.
- Modify the code according to your specific requirements.

## Example Usage
```python
# Importing necessary libraries
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the values of environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = int(os.getenv("DB_PORT"))

# Import the Database class from the utilities module
from utilities.classes.database import Database

# Create an instance of the Database class
db = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE, port=DB_PORT)

# Connect to the database
db.connect()

# Execute queries or prepared queries

# Example:
# results = db.execute_query("SELECT * FROM table_name")
# results = db.execute_prepared_query("SELECT * FROM table_name WHERE id = ?", (1,))

# Disconnect from the database when finished
db.disconnect()

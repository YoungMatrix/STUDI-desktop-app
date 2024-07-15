# File verified

# Importing necessary libraries
import sys
import os
import unittest

# Get the absolute path of the parent directory by navigating one level up from the current file's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Append the parent directory to the Python system path
sys.path.append(parent_dir)

# Import the 'execute_query_from_file' function from database.py
try:
    from utilities.functions.database import execute_query_from_file
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'execute_query_from_file' function could not be found. Ensure the correct path and file exist.")

# Import the Database class from the utilities module
try:
    from utilities.classes.database import Database
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'Database' class could not be found. Ensure the correct path and file exist.")

# Import the configuration settings
try:
    from configuration import config
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'config' file could not be found. Ensure the correct path and file exist.")

# Test class for Database functionality
class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Class-level setup method to initialize database connection parameters
        from the configuration file before any tests are run.
        """
        cls.DB_HOST = config.DB_HOST
        cls.DB_USER = config.DB_USER
        cls.DB_PASSWORD = config.DB_PASSWORD
        cls.DB_DATABASE = config.DB_DATABASE
        cls.DB_PORT = config.DB_PORT

    def setUp(self):
        """
        Instance-level setup method to create a new Database instance and
        connect to the database before each individual test.
        """
        self.db = Database(host=self.DB_HOST, user=self.DB_USER, password=self.DB_PASSWORD, database=self.DB_DATABASE, port=self.DB_PORT)
        print("\n")
        self.db.connect()

    def test_execute_prepared_query(self):
        """
        Test case for the 'execute_prepared_query' method to verify that it works correctly.
        Checks the result type, length, and the type of the first element.
        """
        result = execute_query_from_file(self.db, "app/assets/sql/count_doctors_by_last_name.sql", ("GORGIO",))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0][0], int)
        print("test_execute_prepared_query: OK")
        
    def test_execute_query(self):
        """
        Test case for the 'execute_query' method to verify that it works correctly.
        Checks the result type, length, and the type of the first element.
        """
        result = execute_query_from_file(self.db, "app/assets/sql/count_doctors.sql")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0][0], int)
        print("test_execute_query: OK")
    
    def tearDown(self):
        """
        Instance-level teardown method to disconnect from the database after
        each individual test is run.
        """
        if self.db.connection:
            self.db.disconnect()

# Run the unit tests if this script is executed directly
if __name__ == "__main__":
    unittest.main()

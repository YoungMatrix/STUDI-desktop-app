# File verified

# Import necessary libraries
import mysql.connector

# Database class for managing database connections
class Database:
    _instance = None

    # Constructor to create a new Database instance
    def __new__(cls, *args, **kwargs):
        """
        Ensure that only one instance of the Database class is created (singleton pattern).
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    # Initialize the Database instance
    def __init__(self, host, user, password, database, port):
        """
        Initialize the Database instance with connection details.
        
        :param host: The hostname or IP address of the MySQL server.
        :param user: The username to connect to the MySQL server.
        :param password: The password to connect to the MySQL server.
        :param database: The name of the database to use.
        :param port: The port number to use for the MySQL connection.
        """
        if self.__initialized:
            return
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.__initialized = True

    # Method to check if the database connection is active
    def is_connected(self):
        """
        Check if the database connection is active.
        
        :return: True if connected, False otherwise.
        """
        return self.connection.is_connected() if self.connection else False

    # Method to establish a database connection
    def connect(self):
        """
        Establish a connection to the MySQL database.
        
        :return: True if connection is successful, False otherwise.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                print("Connected to database successfully!")
                return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        return False

    # Method to disconnect from the database
    def disconnect(self):
        """
        Close the database connection if it is active.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from database.")
        else:
            print("No active connection to disconnect.")

    # Method to execute a query on the database
    def execute_query(self, query, params=None):
        """
        Execute a SQL query on the database.
        
        :param query: The SQL query to execute.
        :param params: Optional parameters for the SQL query.
        :return: The result of the query if successful, None otherwise.
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

    # Method to execute a prepared query on the database
    def execute_prepared_query(self, query, params):
        """
        Execute a prepared SQL query on the database.
        
        :param query: The SQL query to execute.
        :param params: The parameters for the SQL query.
        :return: The result of the query if successful, None otherwise.
        """
        cursor = None
        try:
            cursor = self.connection.cursor(prepared=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()

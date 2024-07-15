# File verified

# Function to execute an SQL query from a file
def execute_query_from_file(db, filepath, params=None):
    """
    Reads an SQL query from a file, executes it with the given parameters (if any), and returns the result.
    
    :param db: Database instance
    :param filepath: Path to the SQL file
    :param params: Optional parameters for the prepared query
    :return: Result of the query execution
    """
    try:
        # Open the SQL file containing the query
        with open(filepath, "r") as file:
            query = file.read()

        # Execute the prepared query with parameters if provided
        if params is not None:
            result = db.execute_prepared_query(query, params)
        else:
            result = db.execute_query(query)
        
        return result
    except Exception as e:
        print(f"An error occurred while executing the query from {filepath}: {e}")
        return None

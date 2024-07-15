# Importing necessary libraries
import sys
import os

# Get the absolute path of the parent directory by navigating two levels up from the current file's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Append the parent directory to the Python system path
sys.path.append(parent_dir)

# Import the create_app function from the utilities module
try:
    from utilities.functions.gui import create_app
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'create_app' function could not be found. Ensure the correct path and file exist.")

# Function to display the public view
def publicView():
    root = create_app()
    root.mainloop()

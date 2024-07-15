# File verified

# Import the public view
try:
    from view.public.public_view import publicView
except ModuleNotFoundError:
    raise ModuleNotFoundError("The public view could not be found. Ensure the correct path and file exist.")

# Main Function
def main():
    publicView()

# Check if the script is being run directly
if __name__ == "__main__":
    # Call the main function
    main()

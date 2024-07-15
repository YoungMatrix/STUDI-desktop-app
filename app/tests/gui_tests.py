# File verified

# Importing necessary libraries
from datetime import date, datetime
import sys
import os
import unittest
from unittest.mock import MagicMock, Mock, patch

# Get the absolute path of the parent directory by navigating one level up from the current file's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Append the parent directory to the Python system path
sys.path.append(parent_dir)

# Import the functions to create the GUI and other necessary components
try:
    from utilities.functions.gui import (create_app, gui_connection, gui_patient_information, confirm_date, 
                                         confirm_connection, on_patient_double_click, create_label, create_label_title, toggle_password_visibility)
except ModuleNotFoundError:
    raise ModuleNotFoundError("One or more required functions could not be found. Ensure the correct path and file exist.")

# Import the configuration settings
try:
    from configuration import config
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'config' file could not be found. Ensure the correct path and file exist.")

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

# Dummy Secretary class for testing
class Secretary:
    def __init__(self, last_name):
        self.last_name = last_name

# Test class for GUI
class TestGUI(unittest.TestCase):
    def test_create_and_destroy_app(self):
        """
        Test case to verify the creation and destruction of the main GUI.
        """
        try:
            # Call the function to create the main GUI
            root = create_app()
            root.update()  # Update the GUI to ensure it's fully initialized
            root.destroy()  # Destroy the GUI window

            # Successfully created and destroyed the GUI without exceptions
            print("\ntest_create_and_destroy_app: OK")

        except Exception as e:
            self.fail(f"Exception raised: {e}")

    def test_gui_connection(self):
        """
        Test case to verify the creation and destruction of the connection GUI.
        """
        try:
            # Create a dummy secretary object
            dummy_secretary = Secretary(last_name="TestSurname")

            # Call the function to create the connection GUI
            root = gui_connection(dummy_secretary)
            root.update()  # Update the GUI to ensure it's fully initialized
            root.destroy()  # Destroy the GUI window

            # Successfully created and destroyed the GUI without exceptions
            print("\ntest_gui_connection: OK")

        except Exception as e:
            self.fail(f"Exception raised: {e}")

    def test_gui_patient_information(self):
        """
        Test the GUI for displaying patient information.
        """
        try:
            # Convert string dates to datetime.date objects
            entrance_date = datetime.strptime("2024-06-01", "%Y-%m-%d").date()
            release_date = datetime.strptime("2024-06-10", "%Y-%m-%d").date()
            prescription_date = datetime.strptime("2024-06-01", "%Y-%m-%d").date()
            start_date = datetime.strptime("2024-06-01", "%Y-%m-%d").date()
            end_date = datetime.strptime("2024-06-10", "%Y-%m-%d").date()

            # Create a dummy History object and a dummy Prescription object
            history_data = History("1", "Douleur", "Médecine Générale", "SMITH", entrance_date, release_date)
            prescription_data = Prescription("1", "Soin", prescription_date, start_date, end_date, "Grippe", 
                                            [("Med1", "Medication 1", "1* | Soir"), ("Med2", "Medication 2", "1* | Matin")])
            
            # Create a dummy Patient object for testing with both history and prescription
            dummy_patient = Patient(1, "Doe", "John", "123 Main St", "john.doe@example.com", history_data, prescription_data)
            root_with_prescription = gui_patient_information(dummy_patient)
            root_with_prescription.update()  # Update the GUI to ensure it's fully initialized
            root_with_prescription.destroy()
            print("\ntest_gui_patient_information with prescription: OK")

            # Create a dummy Patient object for testing without prescription
            dummy_patient = Patient(1, "Doe", "John", "123 Main St", "john.doe@example.com", history_data)
            root_without_prescription = gui_patient_information(dummy_patient)
            root_without_prescription.update()  # Update the GUI to ensure it's fully initialized
            root_without_prescription.destroy()
            print("\ntest_gui_patient_information without prescription: OK")

        except Exception as e:
            self.fail(f"Exception raised: {e}")

# Test class for GUI functionalities
class TestGUIFunctionalities(unittest.TestCase):
    @patch("utilities.functions.gui.success_secretary_retrieval")
    @patch("utilities.functions.gui.messagebox")
    @patch("utilities.functions.gui.gui_connection")
    def test_confirm_connection(self, mock_gui_connection, mock_messagebox, mock_success_secretary_retrieval):
        """
        Test case to verify the behavior of the confirm_connection function.

        :param mock_gui_connection: Mock object for gui_connection function.
        :param mock_messagebox: Mock object for messagebox.showerror function.
        :param mock_success_secretary_retrieval: Mock object for success_secretary_retrieval function.
        :return: None
        """
        # Case 1: success_secretary_retrieval returns True, gui_connection called with True
        mock_success_secretary_retrieval.return_value = True
        confirm_connection("test@example.com", "password123")
        mock_gui_connection.assert_called_once_with(True)

        # Case 2: success_secretary_retrieval returns None (incorrect password), messagebox.showerror called with appropriate message
        mock_success_secretary_retrieval.return_value = None
        confirm_connection("test@example.com", "incorrect_password")
        mock_messagebox.showerror.assert_called_once_with("Erreur", "E-mail/Mot de passe incorrects")

        print("\ntest_confirm_connection: OK")

    @patch("utilities.functions.gui.success_patient_list_retrieval")
    def test_confirm_date(self, mock_success_patient_list_retrieval):
        """
        Test case to verify the behavior of confirm_date function.
        
        :param mock_success_patient_list_retrieval: Mock object for success_patient_list_retrieval function.
        :return: None
        """
        try:
            # Create a dummy Calendar widget
            class DummyCalendar:
                def get_date(self):
                    return "02/06/2024"

            # Create a dummy Table widget
            class DummyTable:
                def __init__(self):
                    self.rows = []

                def insert(self, index, position, values):
                    self.rows.append(values)

                def get_children(self):
                    return self.rows

                def delete(self, item):
                    self.rows.remove(item)

            # Mocking the patient list retrieved from the database
            patient_list = [
                Patient(1, "Doe", "John", "123 Main St", "john.doe@example.com"),
                Patient(2, "Smith", "Jane", "456 Elm St", "jane.smith@example.com"),
            ]

            mock_success_patient_list_retrieval.return_value = patient_list

            # Call the function to confirm the selected date
            dummy_cal = DummyCalendar()
            dummy_table = DummyTable()
            returned_patient_list = confirm_date(dummy_cal, dummy_table)

            # Check if the patient list is correctly populated in the table
            self.assertEqual(len(returned_patient_list), len(patient_list))
            self.assertEqual(dummy_table.rows[0], (1, "Doe", "John", "123 Main St", "john.doe@example.com"))
            self.assertEqual(dummy_table.rows[1], (2, "Smith", "Jane", "456 Elm St", "jane.smith@example.com"))

            print("\ntest_confirm_date: OK")

        except Exception as e:
            self.fail(f"Exception raised: {e}")
    
    @patch("utilities.functions.gui.tk.Label")
    def test_create_label(self, mock_label):
        """
        Test the create_label function to verify that a label is created and the text is properly truncated if necessary.

        :param mock_label: Mock object for tk.Label.
        :return: None
        """
        try:
            canvas = Mock()
            text = "This is a long text that should be truncated if it exceeds the maximum width"
            y_position = 50
            max_width = 100

            create_label(canvas, text, y_position, max_width)
            
            # Check if the label is created
            mock_label.assert_called_once()
            
            # Check if the window object is created on the canvas
            canvas.create_window.assert_called_once_with(10, y_position, window=mock_label.return_value, anchor="w")

            print("\ntest_create_label: OK")

        except Exception as e:
            self.fail(f"Exception raised: {e}")

    @patch("utilities.functions.gui.tk.Label")
    def test_create_label_title(self, mock_label):
        """
        Test the create_label_title function to verify that a label is created and positioned correctly on the canvas.

        :param mock_label: Mock object for tk.Label.
        :return: None
        """
        try:
            canvas = Mock()
            text = "Test Title"
            y_position = 50

            create_label_title(canvas, text, y_position)
            
            # Check if the label is created
            mock_label.assert_called_once_with(canvas, text=text, font=(config.FONT_NAME, 15, "bold", "italic"), bg="#f0f0f0", fg="black")

            # Check if the window object is created on the canvas
            canvas.create_window.assert_called_once_with(10, y_position, window=mock_label.return_value, anchor="w")

            print("\ntest_create_label_title: OK")

        except Exception as e:
            self.fail(f"Exception raised: {e}")

    @patch("utilities.functions.gui.success_information_patient_retrieval")
    @patch("utilities.functions.gui.gui_patient_information")
    def test_on_patient_double_click(self, mock_gui_patient_information, mock_success_information_patient_retrieval):
        """
        Test the on_patient_double_click function to verify its behavior when a patient is double-clicked.

        :param mock_gui_patient_information: Mock object for gui_patient_information function.
        :param mock_success_information_patient_retrieval: Mock object for success_information_patient_retrieval function.
        :return: None
        """
        try:
            # Mock event, table, and calendar
            event_mock = Mock()
            table_mock = Mock()
            cal_mock = Mock()

            # Mock data for selected item
            selected_item_data = {
                'values': [1, 'Doe', 'John', '123 Main St', 'john.doe@example.com']
            }

            # Set up the mock table item
            table_mock.item.return_value = selected_item_data

            # Set up mock return value for get_date method of calendar widget
            cal_mock.get_date.return_value = "01/01/2023"

            # Mock the Patient class
            with patch("utilities.functions.gui.Patient", autospec=True) as MockPatient:
                # Create a mock Patient instance
                mock_patient = MockPatient.return_value

                # Mock the success_information_patient_retrieval function
                mock_success_information_patient_retrieval.return_value = mock_patient

                # Call the function to be tested
                on_patient_double_click(event_mock, table_mock, cal_mock)

                # Check if success_information_patient_retrieval is called with the correct arguments
                mock_success_information_patient_retrieval.assert_called_once_with(
                    mock_patient,
                    date(2023, 1, 1)
                )

                # Check if gui_patient_information is called with the correct argument
                mock_gui_patient_information.assert_called_once_with(
                    mock_patient
                )

            print("\ntest_on_patient_double_click: OK")

        except Exception as e:
            self.fail(f"Exception raised: {e}")

    def test_toggle_password_visibility(self):
        """
        Test the toggle_password_visibility function.
        """
        # Create mocks for the password_entry and show_password_button widgets
        password_entry = MagicMock()
        show_password_button = MagicMock()

        # Test toggling password visibility from hidden to shown
        password_entry.__getitem__.return_value = "*"
        toggle_password_visibility(password_entry, show_password_button)
        password_entry.__setitem__.assert_called_with("show", "")
        show_password_button.__setitem__.assert_called_with("text", "Masquer")

        # Reset the mocks
        password_entry.reset_mock()
        show_password_button.reset_mock()

        # Test toggling password visibility from shown to hidden
        password_entry.__getitem__.return_value = ""
        toggle_password_visibility(password_entry, show_password_button)
        password_entry.__setitem__.assert_called_with("show", "*")
        show_password_button.__setitem__.assert_called_with("text", "Afficher")

        print("\ntest_toggle_password_visibility: OK")

if __name__ == "__main__":
    unittest.main()

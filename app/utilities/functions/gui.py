# File verified

# Import necessary libraries
import html
import platform
import sys
import os
import tkinter as tk
from tkinter import Scrollbar, font, messagebox
from tkinter import ttk
from tkinter.ttk import Style, Treeview
from tkcalendar import Calendar
from datetime import datetime

# Get the absolute path of the parent directory by navigating two levels up from the current file's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Append the parent directory to the Python system path
sys.path.append(parent_dir)

# Import the function to retrieve the secretary from the database
try:
    from controller.secretary_controller import success_secretary_retrieval
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'success_secretary_retrieval' function could not be found. Make sure the correct path and file exist.")

# Import the functions to retrieve the patients with their information from the database
try:
    from controller.patient_controller import success_patient_list_retrieval, success_information_patient_retrieval
except ModuleNotFoundError:
    raise ModuleNotFoundError("The 'success_patient_list_retrieval' and 'success_information_patient_retrieval' functions could not be found. Make sure the correct path and file exist.")

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

# Function to create the GUI application
def create_app():
    # Create the main window
    root = tk.Tk()
    root.title("Application bureautique")
    if platform.system() == "Darwin":  # macOS
        canvas_height = 615
        canvas_width = 250
    else:  # Windows or Linux
        canvas_height = 725
        canvas_width = 280
    root.geometry(str(canvas_width * 2) + "x" + str(canvas_height // 2))
    root.resizable(False, False)

    # Bind the function quit_app to the window closing event
    root.protocol("WM_DELETE_WINDOW", lambda: quit_app(root))

    # Create a canvas for layout
    canvas = tk.Canvas(root, bg="#f0f0f0", highlightbackground="#f0f0f0", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Title centered in red, bold, and italic
    title_label = tk.Label(canvas, text="SoignePro", font=(config.FONT_NAME, 24, "bold", "italic"), bg="#f0f0f0", fg="red")
    canvas.create_window(canvas_width, 25, window=title_label)

    # Description of the application
    description_text = (
        "Application à destination des secrétaires de l’hôpital SoigneMoi.\n"
        "Celle-ci permet de consulter les entrées et sorties des patients d'aujourd'hui.\n"
        "Celle-ci permet également de consulter tous les détails de leur séjour."
    )

    # Text widget to display the description
    text_widget = tk.Text(root, wrap="word", font=(config.FONT_NAME, 12), bg="#f0f0f0", fg="black", highlightthickness=0)
    text_widget.insert(tk.END, description_text)
    text_widget.tag_configure("center", justify="center")
    text_widget.tag_add("center", "1.0", "end")

    # Make "SoignePro" bold and italic
    start_idx = description_text.find("SoigneMoi")
    end_idx = start_idx + len("SoigneMoi")
    text_widget.tag_add("bold_italic", f"1.{start_idx}", f"1.{end_idx}")
    bold_italic_font = font.Font(text_widget, text_widget.cget("font"))
    bold_italic_font.configure(weight="bold", slant="italic")
    text_widget.tag_configure("bold_italic", font=bold_italic_font)

    # Create a window for the text widget with specified dimensions
    if platform.system() == "Darwin":  # macOS
        canvas.create_window(canvas_width, 75, height=50, window=text_widget)
    else:  # Windows or Linux
        canvas.create_window(canvas_width, 100, height=60, width=canvas_width * 2, window=text_widget)

    # Create a frame for the textboxes and buttons with rounded corners
    form_frame = tk.Frame(root, width=200, bg="#f0f0f0")
    if platform.system() == "Darwin":  # macOS
        canvas.create_window(canvas_width, 195, window=form_frame)
    else:  # Windows or Linux
        canvas.create_window(canvas_width, 245, window=form_frame)

    # Create textboxes for e-mail and password
    email_label = tk.Label(form_frame, text="E-mail:", font=(config.FONT_NAME, 12), bg="#f0f0f0", fg="black")
    email_label.pack(fill="both", pady=(5, 0))

    email_entry = tk.Entry(form_frame, font=(config.FONT_NAME, 12), bg="white", fg="black", highlightthickness=0)
    email_entry.pack(fill="both", pady=(0, 5))

    password_label = tk.Label(form_frame, text="Password:", font=(config.FONT_NAME, 12), bg="#f0f0f0", fg="black")
    password_label.pack(fill="both", pady=(5, 0))

    password_entry = tk.Entry(form_frame, font=(config.FONT_NAME, 12), show='*', bg="white", fg="black", highlightthickness=0)
    password_entry.pack(fill="both", pady=(0, 10))

    # Create a button to show/hide password
    show_password_button = ttk.Button(form_frame, text="Afficher", command=lambda: toggle_password_visibility(password_entry, show_password_button))
    show_password_button.pack(expand=True, fill="both", pady=(5, 0))

    # Create a confirm button
    confirm_button = ttk.Button(form_frame, text="Confirmer", command=lambda: confirm_connection(email_entry.get(), password_entry.get()))
    confirm_button.pack(expand=True, fill="both", pady=(5, 0))

    # Create a quit button
    quit_button = ttk.Button(form_frame, text="Quitter", command=lambda: quit_app(root))
    quit_button.pack(expand=True, fill="both", pady=(5, 0))

    # Return the root
    return root

# Function to create the GUI connection
def gui_connection(secretary):
    """
    Create a GUI window for the secretary.

    :param secretary: Secretary object containing information about the secretary.
    :return: Tkinter window object.
    """
    # Create the main window
    root = tk.Tk()
    root.title("Application bureautique")
    canvas_height = 1155
    if platform.system() == "Darwin":  # macOS
        canvas_width = 250
    else:  # Windows or Linux
        canvas_width = 290
    root.geometry(str(canvas_width * 2) + "x" + str(canvas_height // 2))
    root.resizable(False, False)

    # Create a canvas for layout
    canvas = tk.Canvas(root, bg="#f0f0f0", highlightbackground="#f0f0f0", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Title centered in red, bold, and italic
    title_label = tk.Label(canvas, text="SoignePro", font=(config.FONT_NAME, 24, "bold", "italic"), bg="#f0f0f0", fg="red")
    canvas.create_window(canvas_width, 25, window=title_label)

    # Description of the application
    description_text = (
        "Bienvenue " + str(secretary.last_name) + "\n"
        "Veuillez sélectionner une date afin de retrouver les patients à l'ordre de ce jour:"
    )

    # Text widget to display the description
    text_widget = tk.Text(root, wrap="word", font=(config.FONT_NAME, 12), bg="#f0f0f0", fg="black", highlightthickness=0)
    text_widget.insert(tk.END, description_text)
    text_widget.tag_configure("center", justify="center")
    text_widget.tag_add("center", "1.0", "end")

    # Make "last name" bold and italic
    start_idx = description_text.find(secretary.last_name)
    end_idx = start_idx + len(secretary.last_name)
    text_widget.tag_add("bold_italic", f"1.{start_idx}", f"1.{end_idx}")
    bold_italic_font = font.Font(text_widget, text_widget.cget("font"))
    bold_italic_font.configure(weight="bold", slant="italic")
    text_widget.tag_configure("bold_italic", font=bold_italic_font)

    # Create a window for the text widget with specified dimensions
    canvas.create_window(canvas_width, 80, height=50, window=text_widget)

    # Create a Calendar widget to choose the date
    today = datetime.now()
    calendar_frame = tk.Frame(root, bg="#f0f0f0", bd=1, relief="solid")
    if platform.system() == "Darwin":  # macOS
        calendar_frame.place(x=canvas_width / 2, y=100, width=250, height=180)
    else:  # Windows or Linux
        calendar_frame.place(x=canvas_width / 2 + 20, y=120, width=250, height=180)
    cal = Calendar(calendar_frame, font=(config.FONT_NAME, 12), selectmode="day", year=today.year, month=today.month, day=today.day, 
                   background="white", foreground="black", selectforeground="red")
    cal.pack(fill="both", expand=True)

    # Create a frame for the table
    table_width = canvas_width * 2 - 20
    table_height = 200
    table_frame = tk.Frame(root, bg="#f0f0f0")
    if platform.system() == "Darwin":  # macOS
        table_frame.place(x=10, y=300, width=table_width, height=table_height)
    else:  # Windows or Linux
        table_frame.place(x=10, y=310, width=table_width, height=table_height)
    
    # Create the table
    columns = ("ID", "Nom", "Prénom", "Adresse", "Email")
    table = Treeview(table_frame, columns=columns, show="headings")
    
    # Center align the table columns
    style = Style()
    style.configure("Treeview.Heading", anchor="center")
    style.configure("Treeview", rowheight=25)
    for column in columns:
        table.heading(column, text=column, anchor="center")
        table.column(column, width=table_width // 5 - 10, anchor="center")

    # Add vertical scrollbar
    vsb = Scrollbar(table_frame, orient="vertical", command=table.yview)
    vsb.pack(side="right", fill="y")
    table.configure(yscrollcommand=vsb.set)

    # Add horizontal scrollbar
    hsb = Scrollbar(table_frame, orient="horizontal", command=table.xview)
    hsb.pack(side="bottom", fill="x")
    table.configure(xscrollcommand=hsb.set)

    # Bind the select event to the on_patient_double_click function
    table.bind('<Double-1>', lambda event:on_patient_double_click(event, table, cal))

    # Display the table
    table.pack(fill="both", expand=True)

    # Create a frame for the textboxes and buttons with rounded corners
    form_frame = tk.Frame(root, width=200, bg="#f0f0f0")
    canvas.create_window(canvas_width, 535, window=form_frame)

    # Create a confirm button
    confirm_button = ttk.Button(form_frame, text="Confirmer", command=lambda: confirm_date(cal, table))
    confirm_button.pack(expand=True, fill="both", pady=(5, 0))

    # Create a return button
    return_button = ttk.Button(form_frame, text="Retour", command=root.destroy)
    return_button.pack(expand=True, fill="both", pady=(5, 0))

    # Return the root
    return root

# Function to create the GUI patient information
def gui_patient_information(update_patient):
    """
    Create a GUI window for displaying patient information.
    """
    # Create the main window
    root = tk.Tk()
    root.title("Application bureautique")
    if platform.system() == "Darwin":  # macOS
        canvas_width = 150
    else:  # Windows or Linux
        canvas_width = 200
    first_position = 60
    distance_position = 30

    # Create a canvas for layout
    canvas = tk.Canvas(root, bg="#f0f0f0", highlightbackground="#f0f0f0", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Title centered in red, bold, and italic
    title_label = tk.Label(canvas, text="SoignePro", font=(config.FONT_NAME, 24, "bold", "italic"), bg="#f0f0f0", fg="red")
    canvas.create_window(canvas_width, 25, window=title_label)

    # List of historical details
    history_details = ["Motif", "Spécialité", "Docteur", "Date d'entrée", "Date de sortie"]

    # List of patient history attributes
    patient_history_attributes = ["pattern", "field", "doctor", "entrance_date", "release_date"]

    # History section aligned to the left
    create_label_title(canvas, "Informations de séjour du patient:", first_position)

    # Initial position for the first element
    next_position = first_position + distance_position

    # Adding historical details using a for loop
    for detail, attribute in zip(history_details, patient_history_attributes):
        # Check if update_patient.history is not None
        if update_patient.history:
            # Get the value of the attribute dynamically
            attribute_value = getattr(update_patient.history, attribute)
        else:
            # Set attribute_value to "-"
            attribute_value = "-"
        # Create and display a label for each historical detail and patient attribute
        create_label(canvas, f"{detail}: {attribute_value}", next_position, canvas_width)
        # Increment the position for the next detail
        next_position += distance_position

    # Check if update_patient.prescription is not None
    if update_patient.prescription is not None:
        # List of prescription details
        prescription_details = ["Label", "Date de prescription", "Date de début", "Date de fin", "Description"]

        # List of patient prescription attributes
        patient_prescription_attributes = ["label", "prescription_date", "start_date", "end_date", "description"]

        # Prescription section aligned to the left
        create_label_title(canvas, "Prescription du docteur:", next_position)

        # Initial position for the next element
        next_position += distance_position

        # Adding historical details using a for loop
        for detail, attribute in zip(prescription_details, patient_prescription_attributes):
            # Get the value of the attribute dynamically
            attribute_value = getattr(update_patient.prescription, attribute)

            # Create and display a label for each historical detail and patient attribute
            create_label(canvas, f"{detail}: {attribute_value}", next_position, canvas_width)
            
            # Increment the position for the next detail
            next_position += distance_position

        if len(update_patient.prescription.medication_details) > 1:
            # Medication section title
            medication_title = "Médicaments et posologies:"
        else:
            medication_title = "Médicament et posologie:"

        # Display the medication section title
        create_label_title(canvas, medication_title, next_position)

        # Increment the position for the next element
        next_position += distance_position

        # Adding medication details using a for loop
        for detail in update_patient.prescription.medication_details:
            # Create and display a label for each medication detail
            create_label(canvas, f"→ {detail[1]} [{detail[2]}]", next_position, canvas_width)

            # Increment the position for the next detail
            next_position += distance_position
    else:
        # Create and display a label indicating no prescription available
        create_label_title(canvas, "Prescription du docteur à venir.", next_position)

        # Increment the position for the next element
        next_position += distance_position

    # Create a frame for the textboxes and buttons with rounded corners
    form_frame = tk.Frame(root, width=200, bg="#f0f0f0")
    canvas.create_window(canvas_width, next_position, window=form_frame)

    # Increment the position for the next element
    next_position += distance_position

    # Create a return button
    return_button = ttk.Button(form_frame, text="Retour", command=root.destroy)
    return_button.pack(expand=True, fill="both", pady=(5, 0))

    # Adjust the main window especially for the height
    canvas_height = next_position
    root.geometry(str(canvas_width * 2) + "x" + str(canvas_height))
    root.resizable(False, False)

    # Return the root
    return root

# Function to handle click event on the confirm button
def confirm_connection(email, password):
    """
    Handle the click event on the confirm button.

    :param email: Email entered by the user.
    :param password: Password entered by the user.
    """
    # Retrieve the secretary using the provided email and password
    secretary = success_secretary_retrieval(email, password)

    # Check if secretary retrieval was successful
    if secretary == False:
        messagebox.showerror("Erreur", "Erreur réseau. Veuillez contacter l'administrateur.")
    elif secretary is None:
        messagebox.showerror("Erreur", "E-mail/Mot de passe incorrects")
    else:
        gui_connection(secretary)

# Function to confirm retrieve the list of patients from the selected date
def confirm_date(cal, table):
    """
    Confirm the selected date from the calendar interface then retrieve the list of patients.

    :param cal: Calendar object.
    :param table: Treeview object to display the list of patients.
    """
    try:
        # Try to parse the date with the first format
        selected_date = datetime.strptime(cal.get_date(), "%d/%m/%Y").date()
    except ValueError:
        try:
            # Try to parse the date with the second format
            selected_date = datetime.strptime(cal.get_date(), "%m/%d/%y").date()
        except ValueError:
            # Handle the case where neither format works
            messagebox.showerror("Erreur", "Format de date incorrect. Veuillez contacter l'administrateur.")
            return []

    # Retrieve the list of patients for the selected date
    patientList = success_patient_list_retrieval(selected_date)

    # Clear previous table data if exists
    for item in table.get_children():
        table.delete(item)

    # Check if the return value is empty, indicating no patients found or a connection error
    if patientList is None:
        messagebox.showerror("Erreur", "Erreur réseau. Veuillez contacter l'administrateur.")
    elif not patientList:
        # Extract only the date part (without time)
        selected_date_without_time = selected_date.strftime("%Y/%m/%d")
        print(f"The list of patients is empty for {selected_date_without_time}.")
    else:
        # Insert the details of each patient into the table
        for patient in patientList:
            table.insert("", "end", values=(patient.id, patient.last_name, patient.first_name, html.unescape(patient.address), patient.email))

    return patientList

# Function triggered when a patient is double-clicked
def on_patient_double_click(event, table, cal):
    """
    Function triggered when a patient is double-clicked.

    :param table: The table containing patient information.
    :param cal: The calendar widget.
    """
    # Get the selected item
    selected_item = event.widget.focus()

    # Get the data of the selected item
    selected_patient_data = table.item(selected_item)

    # Extract the patient ID from the data dictionary
    selected_patient = Patient(
        id=selected_patient_data['values'][0], 
        last_name=selected_patient_data['values'][1], 
        first_name=selected_patient_data['values'][2], 
        address=selected_patient_data['values'][3],
        email=selected_patient_data['values'][4]
    )

    try:
        # Try to parse the date with the first format
        selected_date = datetime.strptime(cal.get_date(), "%d/%m/%Y").date()
    except ValueError:
        try:
            # Try to parse the date with the second format
            selected_date = datetime.strptime(cal.get_date(), "%m/%d/%y").date()
        except ValueError:
            # Handle the case where neither format works
            messagebox.showerror("Erreur", "Format de date incorrect. Veuillez contacter l'administrateur.")

    # Update patient information based on the current date selected in the calendar
    updated_selected_patient = success_information_patient_retrieval(selected_patient, selected_date)

    # If an item is selected
    if updated_selected_patient is None:
        messagebox.showerror("Erreur", "Erreur réseau. Veuillez contacter l'administrateur.")
    else:
        # Open the patient information GUI
        gui_patient_information(updated_selected_patient)

# Function to create a labeled title on the canvas
def create_label_title(canvas, text, y_position):
    """
    Create and display a labeled title on the canvas.

    :param canvas: Tkinter canvas object.
    :param text: Text to display as the title.
    :param y_position: Y position on the canvas where the title will be displayed.
    """
    # Create a label with specified text, font, background color, and foreground color
    title_label = tk.Label(canvas, text=text, font=(config.FONT_NAME, 15, "bold", "italic"), bg="#f0f0f0", fg="black")
    
    # Position the label on the canvas at the specified y_position, anchoring it to the west (left)
    canvas.create_window(10, y_position, window=title_label, anchor="w")

# Function to create a labeled text on the canvas
def create_label(canvas, text, y_position, max_width):
    """
    Create and display a labeled text on the canvas.

    :param canvas: Tkinter canvas object.
    :param text: Text to display on the label.
    :param y_position: Y position on the canvas where the label will be displayed.
    :param max_width: Maximum width for the label before adding "..." to the first line.
    """
    # Split the text into lines
    lines = text.split('\n')
    joined_text = ""
    for line in lines:
        joined_text += line.strip() + ", "
    joined_text = joined_text.rstrip(", ")  # Remove the trailing comma
    
    first_line = lines[0]  # Get the first line of text

    if len(lines) > 1:  # Check if there are more than 1 line
        if len(joined_text) * 2 > max_width:
            joined_text = joined_text[:int(max_width / 3)] + "..."
        text = joined_text
    else:
        if len(first_line) * 2 > max_width:
            first_line = first_line[:int(max_width / 3)] + "..."
        text = first_line

    # Create a label with specified text, font, background color, and foreground color
    label = tk.Label(canvas, text=text, font=(config.FONT_NAME, 12), bg="#f0f0f0", fg="black")
    
    # Position the label on the canvas at the specified y_position, anchoring it to the west (left)
    canvas.create_window(10, y_position, window=label, anchor="w")

# Function to toggle password visibility
def toggle_password_visibility(password_entry, show_password_button):
    """
    Toggle the visibility of the password in the password entry field.

    :param password_entry: Entry widget for password.
    :param show_password_button: Button widget to toggle password visibility.
    """
    if password_entry["show"] == "*":
        password_entry["show"] = ""
        show_password_button["text"] = "Masquer"
    else:
        password_entry["show"] = "*"
        show_password_button["text"] = "Afficher"

# Function to quit the application
def quit_app(root):
    """
    Quit the application after confirmation.

    :param root: Tkinter window object.
    """
    if messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir quitter l'application?"):
        root.destroy()
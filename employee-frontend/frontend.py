'''
CSCI 455 EMRKS Project - Optomet.me Optometry Clinic
Copyright (C) 2024  Julia Dewhurst, Joseph Melancon, Anna Wille, Maya Wyganowska

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import tkinter as tk

from tkinter import messagebox

import mysql.connector

import random


# Function to validate user credentials


def validate_credentials():

    # Get the username and password from the entry fields
    
    server = server_entry.get()

    username = username_entry.get()

    password = password_entry.get()

    # Connect to MySQL database

    try:

        conn = mysql.connector.connect(
            host=server,
            user=username,
            password=password,
            database="Optometry Clinic",
        )

        cursor = conn.cursor()

        if conn.is_connected():

            messagebox.showinfo("Login Successful", "You have successfully logged in!")

            role_selection(username, conn, cursor)

            # function to lead user to the GUI button page

        else:

            messagebox.showerror("Login Failed", "Invalid username or password!")

    except Exception as e:

        messagebox.showerror("Database Error", f"Error: {e}")

    finally:

        # Close the database connection

        if "conn" in locals() or "conn" in globals():

            conn.close()


def role_selection(username, conn, cursor):

    window = tk.Tk()

    window.title("User Actions")

    user_actions = get_user_actions(username, conn, cursor)

    for i in range(len(user_actions)):

        action_button = tk.Button(
            window, text=user_actions[i]["label"], command=user_actions[i]["function"]
        )

        action_button.grid(row=i, column=0, padx=5, pady=5)

    window.mainloop()


def get_user_actions(username, conn, cursor):

    # Define user actions based on username

    if username == "1001":

        return [
            {
                "label": "View Appointment",
                "function": lambda: receptionist_view_appointment(conn, cursor),
            },
            {
                "label": "Check In",
                "function": lambda: receptionist_checkin(conn, cursor),
            },
            {
                "label": "Book Appointment",
                "function": lambda: receptionist_book_appointment(conn, cursor),
            },
            {
                "label": "View Patient Contact",
                "function": lambda: receptionist_view_patient_contact(conn, cursor),
            },
            {
                "label": "Modify Patient Information",
                "function": lambda: receptionist_modify_patient_contact(conn, cursor),
            },
            {
                "label": "Create New Patient File",
                "function": lambda: receptionist_create_patient_file(conn, cursor),
            },
        ]

    elif username == "2001":

        return [
            {
                "label": "View Billing Summary",
                "function": lambda: admin_view_billing_summary(conn, cursor),
            },
            {
                "label": "View Patient Bills",
                "function": lambda: admin_view_patient_bills(conn, cursor),
            },
            {
                "label": "Modify Patient Payment Information",
                "function": lambda: admin_modify_patient_payment(conn, cursor),
            },
            {
                "label": "View Patient Payment",
                "function": lambda: admin_view_patient_payment(conn, cursor),
            },
            {
                "label": "View Patient Contact Information",
                "function": lambda: admin_view_patient_contact(conn, cursor),
            },
            {
                "label": "Create Bill",
                "function": lambda: admin_create_bill(conn, cursor),
            },
        ]

    elif username == "3001":

        return [
            {
                "label": "Log Visit Records",
                "function": lambda: optometrist_log_visit_records(conn, cursor),
            },
            {
                "label": "Create Prescription",
                "function": lambda: optometrist_create_prescription(conn, cursor),
            },
            {
                "label": "View Prescription",
                "function": lambda: optometrist_view_prescription(conn, cursor),
            },
            {
                "label": "View Patient Contact Information",
                "function": lambda: optometrist_view_patient_contact(conn, cursor),
            },
        ]

    elif username == "4001":

        return [
            {
                "label": "View Prescription",
                "function": lambda: optometry_assistant_view_prescription(conn, cursor),
            },
            {
                "label": "Log Visit Records",
                "function": lambda: optometry_assistant_log_visit_records(conn, cursor),
            },
            {
                "label": "View Patient Contact Information",
                "function": lambda: optometry_assistant_view_patient_contact(
                    conn, cursor
                ),
            },
        ]

    else:

        messagebox.showerror("Invalid User", "Invalid username entry")


# Define functions for each action


def receptionist_view_appointment(conn, cursor):

    view_appointment_window = tk.Tk()

    view_appointment_window.title("View Appointments by SSN")

    # Define and place labels and entry fields for patient SSN

    ssn_label = tk.Label(view_appointment_window, text="Enter Patient SSN:")

    ssn_label.grid(row=0, column=0, padx=5, pady=5)

    ssn_entry = tk.Entry(view_appointment_window)

    ssn_entry.grid(row=0, column=1, padx=5, pady=5)

    # Function to search appointments by patient SSN

    def search_appointments():

        # Get patient SSN from entry field

        patient_ssn = ssn_entry.get()

        # Query appointments associated with the given patient SSN

        query = "SELECT * FROM APPOINTMENT WHERE PatientSSN = %s"

        cursor.execute(query, (patient_ssn,))

        appointments = cursor.fetchall()

        # Display the appointments

        if appointments:

            appointment_text = ""

            for appointment in appointments:

                appointment_text += f"Status: {appointment[0]}\n"

                appointment_text += f"Date and Time: {appointment[1]}\n"

                appointment_text += f"Patient SSN: {appointment[3]}\n"

                appointment_text += f"Case ID: {appointment[2]}\n\n"

            messagebox.showinfo("Appointments", appointment_text)

        else:

            messagebox.showinfo(
                "No Appointments", f"No appointments found for SSN {patient_ssn}"
            )

    # Create button to search appointments

    search_button = tk.Button(
        view_appointment_window, text="Search", command=search_appointments
    )

    search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    view_appointment_window.mainloop()


def receptionist_checkin(conn, cursor):

    def search_appointments():

        # Get the search criteria from the entry field

        search_query = search_entry.get()

        # Check if the search query is an SSN

        if search_query.isdigit() and len(search_query) == 9:

            query = (
                "SELECT * FROM APPOINTMENT "
                "WHERE PatientSSN = %s AND Status = 'Scheduled'"
            )

            cursor.execute(query, (search_query,))

        else:

            # Assume the search query is a combination of first and last name

            # Split the query into first and last names

            names = search_query.split()

            if len(names) == 2:

                first_name, last_name = names

                query = (
                    "SELECT * FROM APPOINTMENT "
                    "JOIN PATIENT ON APPOINTMENT.PatientSSN = PATIENT.SSN "
                    "WHERE PATIENT.FName = %s AND PATIENT.LName = %s "
                    "AND Status = 'Scheduled'"
                )

                cursor.execute(query, (first_name, last_name))

            else:

                messagebox.showinfo(
                    "Invalid Search",
                    "Please enter both first name and last name, or a valid SSN.",
                )

                return

        # Fetch the appointment information

        appointments = cursor.fetchall()

        if appointments:

            display_appointments(appointments)

        else:

            messagebox.showinfo(
                "Appointments Not Found",
                "No scheduled appointments found for the given search criteria.",
            )

    def display_appointments(appointments):

        # Clear any previous appointment display

        appointment_listbox.delete(0, tk.END)

        # Display the appointments in the listbox

        for appointment in appointments:

            appointment_listbox.insert(
                tk.END,
                f"Appointment ID: {appointment[2]}, "
                f"Patient SSN: {appointment[3]}, "
                f"Date/Time: {appointment[1]}, "
                f"Status: {appointment[0]}",
            )

    def check_in():

        # Get the selected appointment from the listbox

        selected_index = appointment_listbox.curselection()

        if not selected_index:

            messagebox.showinfo(
                "No Appointment Selected", "Please select an appointment to check-in."
            )

            return

        appointment_id = (
            appointment_listbox.get(selected_index).split(",")[0].split(":")[1].strip()
        )

        # Update the appointment status to "Active" in the database

        update_query = "UPDATE APPOINTMENT SET Status = 'Active' WHERE CaseID = %s"

        cursor.execute(update_query, (appointment_id,))

        conn.commit()

        messagebox.showinfo("Success", "Appointment checked in successfully!")

    # Create a new window for checking in patients

    check_in_window = tk.Toplevel()

    check_in_window.title("Receptionist Check-In")

    # Label and entry field for searching appointments

    search_label = tk.Label(
        check_in_window, text="Search by First Name Last Name or SSN:"
    )

    search_label.grid(row=0, column=0, padx=5, pady=5)

    search_entry = tk.Entry(check_in_window)

    search_entry.grid(row=0, column=1, padx=5, pady=5)

    # Button to search for appointments

    search_button = tk.Button(
        check_in_window, text="Search", command=search_appointments
    )

    search_button.grid(row=0, column=2, padx=5, pady=5)

    # Listbox to display appointments

    appointment_listbox = tk.Listbox(check_in_window, width=50, height=10)

    appointment_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    # Button to check-in

    check_in_button = tk.Button(check_in_window, text="Check-In", command=check_in)

    check_in_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

    check_in_window.mainloop()


def receptionist_book_appointment(conn, cursor):

    # Create a new window for booking appointment

    book_appointment_window = tk.Tk()

    book_appointment_window.title("Book Appointment")

    # Define and place labels and entry fields for appointment information

    """status_label = tk.Label(book_appointment_window, text="Status:")

    status_label.grid(row=0, column=0, padx=5, pady=5)

    status_entry = tk.Entry(book_appointment_window)

    status_entry.grid(row=0, column=1, padx=5, pady=5)"""

    datetime_label = tk.Label(
        book_appointment_window, text="Date and Time (YYYY-MM-DD HH:MM:SS):"
    )

    datetime_label.grid(row=1, column=0, padx=5, pady=5)

    datetime_entry = tk.Entry(book_appointment_window)

    datetime_entry.grid(row=1, column=1, padx=5, pady=5)

    patient_ssn_label = tk.Label(book_appointment_window, text="Patient SSN:")

    patient_ssn_label.grid(row=2, column=0, padx=5, pady=5)

    patient_ssn_entry = tk.Entry(book_appointment_window)

    patient_ssn_entry.grid(row=2, column=1, padx=5, pady=5)

    """case_id_label = tk.Label(book_appointment_window, text="Case ID: ")

    case_id_label.grid(row=3, column=0, padx=5, pady=5)

    case_id_entry = tk.Entry(book_appointment_window)

    case_id_entry.grid(row=3, column=1, padx=5, pady=5)"""

    def generate_unique_case_id(cursor):

        while True:

            case_id = random.randint(100, 999)

            cursor.execute("SELECT * FROM APPOINTMENT WHERE CaseID = %s", (case_id,))

            if not cursor.fetchone():

                return case_id

    # Function to insert appointment data into the database

    def insert_appointment():

        # Get appointment information from entry fields

        status = "Scheduled"

        datetime = datetime_entry.get()

        patient_ssn = patient_ssn_entry.get()

        case_id = generate_unique_case_id(cursor)

        # Insert appointment data into the database

        insert_query = "INSERT INTO APPOINTMENT (Status, DateTime, PatientSSN, CaseID) VALUES (%s, %s, %s, %s)"

        cursor.execute(insert_query, (status, datetime, patient_ssn, case_id))

        conn.commit()

        messagebox.showinfo("Success", "Appointment booked successfully!")

    # Create button to submit appointment information

    submit_button = tk.Button(
        book_appointment_window, text="Submit", command=insert_appointment
    )

    submit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    book_appointment_window.mainloop()


def receptionist_view_patient_contact(conn, cursor):

    def search_patient():

        # Get the search criteria from the entry fields

        search_query = search_entry.get()

        # Check if the search query is an SSN

        if search_query.isdigit() and len(search_query) == 9:

            query = "SELECT Fname, Lname, Email, PhoneNo FROM PATIENT WHERE SSN = %s"

            cursor.execute(query, (search_query,))

        else:

            # Assume the search query is a combination of first and last name

            # Split the query into first and last names

            names = search_query.split()

            if len(names) == 2:

                first_name, last_name = names

                query = (
                    "SELECT Fname, Lname, Email, PhoneNo FROM PATIENT "
                    "WHERE Fname = %s AND Lname = %s"
                )

                cursor.execute(query, (first_name, last_name))

            else:

                messagebox.showinfo(
                    "Invalid Search",
                    "Please enter both first name and last name, or a valid SSN.",
                )

                return

        # Fetch the patient information

        patient_info = cursor.fetchone()

        if patient_info:

            # Display patient contact information

            contact_info_label.config(
                text=f"First Name: {patient_info[0]}\n"
                f"Last Name: {patient_info[1]}\n"
                f"Email: {patient_info[2]}\n"
                f"Phone: {patient_info[3]}\n"
            )

        else:

            messagebox.showinfo(
                "Patient Not Found", "No patient found with the given search criteria."
            )

    # Create a new window for searching patient contact information

    view_contact_window = tk.Toplevel()

    view_contact_window.title("View Patient Contact Information")

    # Label and entry field for searching patient

    search_label = tk.Label(
        view_contact_window, text="Search by First Name Last Name or SSN:"
    )

    search_label.grid(row=0, column=0, padx=5, pady=5)

    search_entry = tk.Entry(view_contact_window)

    search_entry.grid(row=0, column=1, padx=5, pady=5)

    # Button to search for the patient

    search_button = tk.Button(
        view_contact_window, text="Search", command=search_patient
    )

    search_button.grid(row=0, column=2, padx=5, pady=5)

    # Label to display patient contact information

    contact_info_label = tk.Label(view_contact_window, text="")

    contact_info_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    view_contact_window.mainloop()


def receptionist_modify_patient_contact(conn, cursor):

    def search_patient():

        # Get the search criteria from the entry field

        search_query = search_entry.get()

        # Check if the search query is an SSN

        if search_query.isdigit() and len(search_query) == 9:

            query = "SELECT * FROM PATIENT WHERE SSN = %s"

            cursor.execute(query, (search_query,))

        else:

            # Assume the search query is a combination of first and last name

            # Split the query into first and last names

            names = search_query.split()

            if len(names) == 2:

                first_name, last_name = names

                query = "SELECT * FROM PATIENT WHERE FName = %s AND LName = %s"

                cursor.execute(query, (first_name, last_name))

            else:

                messagebox.showinfo(
                    "Invalid Search",
                    "Please enter both first name and last name, or a valid SSN.",
                )

                return

        # Fetch the patient information

        patient_info = cursor.fetchone()

        if patient_info:

            # Open a new window to modify patient contact information

            modify_patient_info_window(patient_info)

        else:

            messagebox.showinfo(
                "Patient Not Found", "No patient found with the given search criteria."
            )

    def modify_patient_info_window(patient_info):

        def modify_patient_info():

            # Get the updated information from the entry fields

            new_fname = fname_entry.get()

            new_lname = lname_entry.get()

            new_email = email_entry.get()

            new_phone = phone_entry.get()

            new_card = card_entry.get()

            new_cvv = cvv_entry.get()

            new_expDate = expDate_entry.get()

            new_CCname = CCname_entry.get()

            # Update the patient's information in the database

            update_query = "UPDATE PATIENT SET FName = %s, LName = %s, Email = %s, PhoneNo = %s, CredCardNo = %s, CVV = %s, ExpDate = %s, CredCardName = %s WHERE SSN = %s"

            cursor.execute(
                update_query,
                (
                    new_fname,
                    new_lname,
                    new_email,
                    new_phone,
                    new_card,
                    new_cvv,
                    new_expDate,
                    new_CCname,
                    patient_info[7],
                ),
            )

            conn.commit()

            messagebox.showinfo("Success", "Patient information updated successfully!")

        # Create a new window for modifying patient contact information

        modify_contact_window = tk.Toplevel()

        modify_contact_window.title("Modify Patient Contact Information")

        # Labels and entry fields for modifying patient contact information

        fname_label = tk.Label(modify_contact_window, text="First Name:")

        fname_label.grid(row=0, column=0, padx=5, pady=5)

        fname_entry = tk.Entry(modify_contact_window)

        fname_entry.grid(row=0, column=1, padx=5, pady=5)

        fname_entry.insert(0, patient_info[0])  # Display current first name

        lname_label = tk.Label(modify_contact_window, text="Last Name:")

        lname_label.grid(row=1, column=0, padx=5, pady=5)

        lname_entry = tk.Entry(modify_contact_window)

        lname_entry.grid(row=1, column=1, padx=5, pady=5)

        lname_entry.insert(0, patient_info[1])  # Display current last name

        email_label = tk.Label(modify_contact_window, text="Email:")

        email_label.grid(row=2, column=0, padx=5, pady=5)

        email_entry = tk.Entry(modify_contact_window)

        email_entry.grid(row=2, column=1, padx=5, pady=5)

        email_entry.insert(0, patient_info[2])  # Display current email

        phone_label = tk.Label(modify_contact_window, text="Phone:")

        phone_label.grid(row=3, column=0, padx=5, pady=5)

        phone_entry = tk.Entry(modify_contact_window)

        phone_entry.grid(row=3, column=1, padx=5, pady=5)

        phone_entry.insert(0, patient_info[3])  # Display current phone

        card_label = tk.Label(modify_contact_window, text="Card No:")

        card_label.grid(row=4, column=0, padx=5, pady=5)

        card_entry = tk.Entry(modify_contact_window)

        card_entry.grid(row=4, column=1, padx=5, pady=5)

        card_entry.insert(0, patient_info[4])  # Display current card no

        cvv_label = tk.Label(modify_contact_window, text="CVV:")

        cvv_label.grid(row=5, column=0, padx=5, pady=5)

        cvv_entry = tk.Entry(modify_contact_window)

        cvv_entry.grid(row=5, column=1, padx=5, pady=5)

        cvv_entry.insert(0, patient_info[5])  # Display current cvv

        expDate_label = tk.Label(modify_contact_window, text="Exp Date:")

        expDate_label.grid(row=6, column=0, padx=5, pady=5)

        expDate_entry = tk.Entry(modify_contact_window)

        expDate_entry.grid(row=6, column=1, padx=5, pady=5)

        expDate_entry.insert(0, patient_info[6])  # Display current exp date

        CCname_label = tk.Label(modify_contact_window, text="CC Name:")

        CCname_label.grid(row=7, column=0, padx=5, pady=5)

        CCname_entry = tk.Entry(modify_contact_window)

        CCname_entry.grid(row=7, column=1, padx=5, pady=5)

        CCname_entry.insert(0, patient_info[8])  # Display current cc name

        # Button to modify patient contact information

        modify_button = tk.Button(
            modify_contact_window, text="Modify", command=modify_patient_info
        )

        modify_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        modify_contact_window.mainloop()

    # Create a new window for searching patient

    search_patient_window = tk.Toplevel()

    search_patient_window.title("Search Patient")

    # Label and entry field for searching patient

    search_label = tk.Label(
        search_patient_window, text="Search by First Name Last Name or SSN:"
    )

    search_label.grid(row=0, column=0, padx=5, pady=5)

    search_entry = tk.Entry(search_patient_window)

    search_entry.grid(row=0, column=1, padx=5, pady=5)

    # Button to search for the patient

    search_button = tk.Button(
        search_patient_window, text="Search", command=search_patient
    )

    search_button.grid(row=0, column=2, padx=5, pady=5)

    search_patient_window.mainloop()


def receptionist_create_patient_file(conn, cursor):

    def add_patient():

        # Get the patient information from the entry fields

        ssn = ssn_entry.get()

        fname = fname_entry.get()

        lname = lname_entry.get()

        email = email_entry.get()

        phone = phone_entry.get()

        card_no = card_entry.get()

        cvv = cvv_entry.get()

        exp_date = exp_date_entry.get()

        cc_name = cc_name_entry.get()

        # Check if the SSN already exists in the database

        check_query = "SELECT * FROM PATIENT WHERE SSN = %s"

        cursor.execute(check_query, (ssn,))

        existing_patient = cursor.fetchone()

        if existing_patient:

            messagebox.showerror("Error", "Patient with this SSN already exists.")

        else:

            # Insert the patient information into the database

            insert_query = (
                "INSERT INTO PATIENT (SSN, FName, LName, Email, PhoneNo, CredCardNo, CVV, ExpDate, CredCardName) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )

            cursor.execute(
                insert_query,
                (ssn, fname, lname, email, phone, card_no, cvv, exp_date, cc_name),
            )

            conn.commit()

            messagebox.showinfo("Success", "Patient file created successfully!")

    # Create a new window for creating a new patient file

    new_patient_window = tk.Toplevel()

    new_patient_window.title("Create New Patient File")

    # Labels and entry fields for patient information

    ssn_label = tk.Label(new_patient_window, text="SSN:")

    ssn_label.grid(row=0, column=0, padx=5, pady=5)

    ssn_entry = tk.Entry(new_patient_window)

    ssn_entry.grid(row=0, column=1, padx=5, pady=5)

    fname_label = tk.Label(new_patient_window, text="First Name:")

    fname_label.grid(row=1, column=0, padx=5, pady=5)

    fname_entry = tk.Entry(new_patient_window)

    fname_entry.grid(row=1, column=1, padx=5, pady=5)

    lname_label = tk.Label(new_patient_window, text="Last Name:")

    lname_label.grid(row=2, column=0, padx=5, pady=5)

    lname_entry = tk.Entry(new_patient_window)

    lname_entry.grid(row=2, column=1, padx=5, pady=5)

    email_label = tk.Label(new_patient_window, text="Email:")

    email_label.grid(row=3, column=0, padx=5, pady=5)

    email_entry = tk.Entry(new_patient_window)

    email_entry.grid(row=3, column=1, padx=5, pady=5)

    phone_label = tk.Label(new_patient_window, text="Phone:")

    phone_label.grid(row=4, column=0, padx=5, pady=5)

    phone_entry = tk.Entry(new_patient_window)

    phone_entry.grid(row=4, column=1, padx=5, pady=5)

    card_label = tk.Label(new_patient_window, text="Card No:")

    card_label.grid(row=5, column=0, padx=5, pady=5)

    card_entry = tk.Entry(new_patient_window)

    card_entry.grid(row=5, column=1, padx=5, pady=5)

    cvv_label = tk.Label(new_patient_window, text="CVV:")

    cvv_label.grid(row=6, column=0, padx=5, pady=5)

    cvv_entry = tk.Entry(new_patient_window)

    cvv_entry.grid(row=6, column=1, padx=5, pady=5)

    exp_date_label = tk.Label(new_patient_window, text="Exp Date YYYY-MM-DD:")

    exp_date_label.grid(row=7, column=0, padx=5, pady=5)

    exp_date_entry = tk.Entry(new_patient_window)

    exp_date_entry.grid(row=7, column=1, padx=5, pady=5)

    cc_name_label = tk.Label(new_patient_window, text="CC Name:")

    cc_name_label.grid(row=8, column=0, padx=5, pady=5)

    cc_name_entry = tk.Entry(new_patient_window)

    cc_name_entry.grid(row=8, column=1, padx=5, pady=5)

    # Button to add the patient

    add_button = tk.Button(new_patient_window, text="Add Patient", command=add_patient)

    add_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

    new_patient_window.mainloop()


def admin_view_billing_summary(conn, cursor):

    billSummary_window = tk.Tk()

    billSummary_window.title("Billing Summary")

    caseIDLabel = tk.Label(billSummary_window, text="Enter Case ID: ")

    caseIDLabel.grid(row=0, column=0, padx=5, pady=5)

    caseIDEntry = tk.Entry(billSummary_window)

    caseIDEntry.grid(row=0, column=1, padx=5, pady=5)

    def searchBill():

        caseID = caseIDEntry.get()

        query = "SELECT * FROM BILLS WHERE CaseID = %s"

        cursor.execute(query, (caseID,))

        bill = cursor.fetchone()

        if bill:

            billSummary = ""

            billSummary += f"Bill ID: {bill[0]}\n"

            billSummary += f"Case ID: {bill[1]}\n"

            billSummary += f"Payment Type: {bill[2]}\n"

            billSummary += f"Details: {bill[3]}\n"

            billSummary += f"Bill Total: ${bill[4]}"

            messagebox.showinfo("Billing Summary", billSummary)

        else:

            messagebox.showinfo(
                "Billing Summary", f"No bill found for Case ID {caseID}"
            )

    searchButton = tk.Button(billSummary_window, text="Search", command=searchBill)

    searchButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    billSummary_window.mainloop()


def admin_view_patient_bills(conn, cursor):

    # Create a new window for viewing patient bills

    view_bills_window = tk.Tk()

    view_bills_window.title("View Patient Bills")

    # Define and place labels and entry fields for patient SSN

    patientSSN_label = tk.Label(view_bills_window, text="Patient SSN:")

    patientSSN_label.grid(row=0, column=0, padx=5, pady=5)

    patientSSN_entry = tk.Entry(view_bills_window)

    patientSSN_entry.grid(row=0, column=1, padx=5, pady=5)

    # Function to search for bills associated with the entered patient SSN

    def search_bills():

        # Get the patient SSN from the entry field

        patientSSN = patientSSN_entry.get()

        # Query the database to retrieve appointments associated with the patient SSN

        query = "SELECT CaseID FROM APPOINTMENTS WHERE PatientSSN = %s"

        cursor.execute(query, (patientSSN,))

        appointments = cursor.fetchall()

        # If appointments are found, retrieve billing summary for each case ID

        if appointments:

            bill_summary = ""

            for appointment in appointments:

                case_id = appointment[0]

                # Query the database to retrieve billing information for the case ID

                query_bill = "SELECT * FROM BILLS WHERE CaseID = %s"

                cursor.execute(query_bill, (case_id,))

                bills = cursor.fetchall()

                for bill in bills:

                    bill_summary += f"Bill ID: {bill[0]}\n"

                    bill_summary += f"Case ID: {bill[1]}\n"

                    bill_summary += f"Amount: ${bill[4]}\n"

                    bill_summary += f"Payment Type: {bill[2]}\n"

                    bill_summary += f"Details: {bill[3]}\n"

            messagebox.showinfo("Patient Bills", bill_summary)

        else:

            messagebox.showinfo(
                "Patient Bills", "No bills found for the entered Patient SSN."
            )

    # Create a button to search for bills

    search_button = tk.Button(view_bills_window, text="Search", command=search_bills)

    search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    view_bills_window.mainloop()


def admin_view_patient_bills(conn, cursor):

    # Create a new window for viewing patient bills

    view_bills_window = tk.Tk()

    view_bills_window.title("View Patient Bills")

    # Define and place labels and entry fields for case ID

    patientSSN_label = tk.Label(view_bills_window, text="Patient SSN:")

    patientSSN_label.grid(row=0, column=0, padx=5, pady=5)

    patientSSN_entry = tk.Entry(view_bills_window)

    patientSSN_entry.grid(row=0, column=1, padx=5, pady=5)

    # Function to search for bills associated with the entered case ID

    def search_bills():

        # Get the case ID from the entry field

        patientSSN = patientSSN_entry.get()

        # Query the database to retrieve bills associated with the case ID

        query = "SELECT * FROM APPOINTMENT WHERE PatientSSN = %s"

        cursor.execute(query, (patientSSN,))

        bills = cursor.fetchall()

        # Display the patient's bills

        if bills:

            bill_summary = ""

            for bill in bills:

                bill_summary += f"Bill ID: {bill[0]}\n"

                bill_summary += f"Case ID: {bill[1]}\n"

                bill_summary += f"Amount: ${bill[4]}\n"

                bill_summary += f"Payment Type: {bill[2]}\n"

                bill_summary += f"Details: {bill[3]}\n"

            messagebox.showinfo("Patient Bills", bill_summary)

        else:

            messagebox.showinfo("Patient Bills", f"No bills found for Case ID {caseID}")

    # Create a button to search for bills

    search_button = tk.Button(view_bills_window, text="Search", command=search_bills)

    search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    view_bills_window.mainloop()


def admin_modify_patient_payment(conn, cursor):

    receptionist_modify_patient_contact(conn, cursor)


def admin_view_patient_payment(conn, cursor):

    # Create a new window for viewing patient payment information

    view_payment_window = tk.Tk()

    view_payment_window.title("View Patient Payment")

    # Define and place labels and entry fields for patient SSN

    ssn_label = tk.Label(view_payment_window, text="Enter Patient SSN:")

    ssn_label.grid(row=0, column=0, padx=5, pady=5)

    ssn_entry = tk.Entry(view_payment_window)

    ssn_entry.grid(row=0, column=1, padx=5, pady=5)

    # Function to display the patient's payment information

    def display_payment():

        # Get the patient's SSN from the entry field

        patient_ssn = ssn_entry.get()

        # Query the database to retrieve the patient's payment information

        query = (
            "SELECT CredCardNo, CVV, ExpDate, CredCardName FROM PATIENT WHERE SSN = %s"
        )

        cursor.execute(query, (patient_ssn,))

        payment_info = cursor.fetchone()

        # Display the patient's payment information

        if payment_info:

            payment_text = ""

            payment_text += f"Name on Card: {payment_info[3]}\n"

            payment_text += f"Credit Card Number: {payment_info[0]}\n"

            payment_text += f"CVV: {payment_info[1]}\n"

            payment_text += f"Expiration Date: {payment_info[2]}\n"

            messagebox.showinfo("Patient Payment Information", payment_text)

        else:

            messagebox.showinfo(
                "Patient Payment Information",
                f"No payment information found for SSN {patient_ssn}",
            )

    # Create a button to display the payment information

    display_button = tk.Button(
        view_payment_window, text="Display", command=display_payment
    )

    display_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    view_payment_window.mainloop()


def admin_create_bill(conn, cursor):

    def generate_unique_bill_id(cursor):

        while True:

            bill_id = random.randint(100, 999)

            cursor.execute("SELECT * FROM BILLS WHERE BillID = %s", (bill_id,))

            if not cursor.fetchone():

                return bill_id

    # Create a new window for creating a bill

    create_bill_window = tk.Tk()

    create_bill_window.title("Create Bill")

    # Define and place labels and entry fields for patient Case ID and bill details

    case_id_label = tk.Label(create_bill_window, text="Enter Case ID:")

    case_id_label.grid(row=0, column=0, padx=5, pady=5)

    case_id_entry = tk.Entry(create_bill_window)

    case_id_entry.grid(row=0, column=1, padx=5, pady=5)

    amount_label = tk.Label(create_bill_window, text="Bill Amount:")

    amount_label.grid(row=1, column=0, padx=5, pady=5)

    amount_entry = tk.Entry(create_bill_window)

    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    # Function to create a bill for the patient

    def create_bill():

        # Get the patient's Case ID and bill amount from the entry fields

        case_id = case_id_entry.get()

        bill_amount = amount_entry.get()

        # Generate a unique 3-digit bill ID

        bill_id = generate_unique_bill_id(cursor)

        # Insert the bill information into the database

        insert_query = "INSERT INTO BILLS (BillID, CaseID, PaymentType, Details, BillTotal) VALUES (%s, %s, %s,%s,%s)"

        cursor.execute(
            insert_query, (bill_id, case_id, "Credit Card", "Unpaid", bill_amount)
        )

        conn.commit()

        # Show success message

        messagebox.showinfo("Success", "Bill created successfully!")

    # Create a button to create the bill

    create_button = tk.Button(
        create_bill_window, text="Create Bill", command=create_bill
    )

    create_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    create_bill_window.mainloop()


def admin_view_patient_contact(conn, cursor):

    receptionist_view_patient_contact(conn, cursor)


def optometrist_log_visit_records(conn, cursor):

    # Create a new window for logging visit records

    log_visit_window = tk.Tk()

    log_visit_window.title("Log Visit Records")

    # Define and place labels and entry fields for case ID and visit notes

    caseLead_label = tk.Label(log_visit_window, text="Case Lead:")

    caseLead_label.grid(row=0, column=0, padx=5, pady=5)

    caseLead_entry = tk.Entry(log_visit_window)

    caseLead_entry.grid(row=0, column=1, padx=5, pady=5)

    case_id_label = tk.Label(log_visit_window, text="Enter Case ID:")

    case_id_label.grid(row=1, column=0, padx=5, pady=5)

    case_id_entry = tk.Entry(log_visit_window)

    case_id_entry.grid(row=1, column=1, padx=5, pady=5)

    notes_label = tk.Label(log_visit_window, text="Visit Notes:")

    notes_label.grid(row=2, column=0, padx=5, pady=5)

    notes_entry = tk.Entry(log_visit_window)

    notes_entry.grid(row=2, column=1, padx=5, pady=5)

    appointmentDescription_label = tk.Label(
        log_visit_window, text="Appointment Description:"
    )

    appointmentDescription_label.grid(row=3, column=0, padx=5, pady=5)

    appointmentDescription_entry = tk.Entry(log_visit_window)

    appointmentDescription_entry.grid(row=3, column=1, padx=5, pady=5)

    # Function to log visit records for the patient

    def log_visit():

        # Get the case ID, visit notes, case lead, and appointment description from the entry fields

        case_id = case_id_entry.get()

        visit_notes = notes_entry.get()

        case_lead = caseLead_entry.get()

        appointment_description = appointmentDescription_entry.get()

        # Insert the visit records into the database

        insert_query = "INSERT INTO APPOINTMENT_NOTES (CaseLeadEmpID, CaseID, CaseNotes, AppointmentDescription) VALUES (%s, %s, %s, %s)"

        cursor.execute(
            insert_query, (case_lead, case_id, visit_notes, appointment_description)
        )

        conn.commit()

        # Show success message

        messagebox.showinfo("Success", "Visit records logged successfully!")

    # Create a button to log visit records

    log_button = tk.Button(log_visit_window, text="Log Visit", command=log_visit)

    log_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    log_visit_window.mainloop()


def optometrist_create_prescription(conn, cursor):

    def generate_unique_prescription_id(cursor):

        # Query the database to get the maximum prescription ID

        cursor.execute("SELECT MAX(PrescriptionID) FROM PRESCRIPTION")

        max_id = cursor.fetchone()[0]

        # If no prescriptions exist yet, set max_id to 0

        if max_id is None:

            max_id = 0

        # Increment the maximum ID by one to get a new unique ID

        prescription_id = max_id + 1

        return prescription_id

    # Create a new window for creating a prescription

    create_prescription_window = tk.Tk()

    create_prescription_window.title("Create Prescription")

    # Define and place labels and entry fields for case ID, start date, expiration date,

    # eyeglass prescription, and prescription ID

    case_id_label = tk.Label(create_prescription_window, text="Enter Case ID:")

    case_id_label.grid(row=0, column=0, padx=5, pady=5)

    case_id_entry = tk.Entry(create_prescription_window)

    case_id_entry.grid(row=0, column=1, padx=5, pady=5)

    start_date_label = tk.Label(create_prescription_window, text="Start Date:")

    start_date_label.grid(row=1, column=0, padx=5, pady=5)

    start_date_entry = tk.Entry(create_prescription_window)

    start_date_entry.grid(row=1, column=1, padx=5, pady=5)

    exp_date_label = tk.Label(create_prescription_window, text="Expiration Date:")

    exp_date_label.grid(row=2, column=0, padx=5, pady=5)

    exp_date_entry = tk.Entry(create_prescription_window)

    exp_date_entry.grid(row=2, column=1, padx=5, pady=5)

    eyeglass_prescription_label = tk.Label(
        create_prescription_window, text="Eyeglass Prescription:"
    )

    eyeglass_prescription_label.grid(row=3, column=0, padx=5, pady=5)

    eyeglass_prescription_entry = tk.Entry(create_prescription_window)

    eyeglass_prescription_entry.grid(row=3, column=1, padx=5, pady=5)

    # Function to create a prescription for the patient

    def create_prescription():

        # Get the input data from the entry fields

        case_id = case_id_entry.get()

        start_date = start_date_entry.get()

        exp_date = exp_date_entry.get()

        eyeglass_prescription = eyeglass_prescription_entry.get()

        # Generate a unique prescription ID

        prescription_id = generate_unique_prescription_id(cursor)

        # Retrieve patient SSN based on case ID from the appointment table

        cursor.execute(
            "SELECT PatientSSN FROM APPOINTMENT WHERE CaseID = %s", (case_id,)
        )

        patient_ssn = cursor.fetchone()

        if patient_ssn:

            patient_ssn = patient_ssn[0]

        else:

            messagebox.showerror("Error", "Invalid Case ID. Patient SSN not found.")

            return

        # Insert prescription information into the database

        insert_query = "INSERT INTO PRESCRIPTION (StartDate, ExpDate, Details, PatientSSN, PrescriptionID, CaseID) VALUES (%s, %s, %s, %s, %s, %s)"

        cursor.execute(
            insert_query,
            (
                start_date,
                exp_date,
                eyeglass_prescription,
                patient_ssn,
                prescription_id,
                case_id,
            ),
        )

        conn.commit()

        # Show success message

        messagebox.showinfo(
            "Success",
            "Prescription created successfully! Prescription ID: "
            + str(prescription_id),
        )

    # Create a button to create the prescription

    create_button = tk.Button(
        create_prescription_window,
        text="Create Prescription",
        command=create_prescription,
    )

    create_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    create_prescription_window.mainloop()


def optometrist_view_patient_contact(conn, cursor):

    receptionist_view_patient_contact(conn, cursor)


def optometrist_view_prescription(conn, cursor):

    optometry_assistant_view_prescription(conn, cursor)


def optometry_assistant_view_prescription(conn, cursor):

    # Create a new window for viewing patient prescription

    view_prescription_window = tk.Tk()

    view_prescription_window.title("View Patient Prescription")

    # Define and place labels and entry fields for patient SSN

    ssn_label = tk.Label(view_prescription_window, text="Enter Patient SSN:")

    ssn_label.grid(row=0, column=0, padx=5, pady=5)

    ssn_entry = tk.Entry(view_prescription_window)

    ssn_entry.grid(row=0, column=1, padx=5, pady=5)

    # Function to display the patient's prescription

    def display_prescription():

        # Get the patient's SSN from the entry field

        patient_ssn = ssn_entry.get()

        # Query the database to retrieve the patient's prescription

        query = "SELECT Details FROM PRESCRIPTION WHERE PatientSSN = %s"

        cursor.execute(query, (patient_ssn,))

        prescription = cursor.fetchone()

        # Display the patient's prescription

        if prescription:

            messagebox.showinfo("Patient Prescription", prescription)

        else:

            messagebox.showinfo(
                "Patient Prescription", f"No prescription found for SSN {patient_ssn}"
            )

    # Create a button to display the prescription

    display_button = tk.Button(
        view_prescription_window, text="Display", command=display_prescription
    )

    display_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    view_prescription_window.mainloop()


def optometry_assistant_log_visit_records(conn, cursor):

    optometrist_log_visit_records(conn, cursor)


def optometry_assistant_view_patient_contact(conn, cursor):

    receptionist_view_patient_contact(conn, cursor)


# Create the main window
root = tk.Tk()

root.title("MySQL Login")


# Create labels and entry fields

server_label = tk.Label(root, text="Server:")

server_label.grid(row=0, column=0, padx=5, pady=5)

server_entry = tk.Entry(root)

server_entry.grid(row=0, column=1, padx=5, pady=5)


username_label = tk.Label(root, text="Username:")

username_label.grid(row=1, column=0, padx=5, pady=5)

username_entry = tk.Entry(root)

username_entry.grid(row=1, column=1, padx=5, pady=5)


password_label = tk.Label(root, text="Password:")

password_label.grid(row=2, column=0, padx=5, pady=5)

password_entry = tk.Entry(root, show="*")

password_entry.grid(row=2, column=1, padx=5, pady=5)


# Create login button

login_button = tk.Button(root, text="Login", command=validate_credentials)

login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


# Run the main event loop

root.mainloop()

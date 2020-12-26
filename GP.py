from tabulate import tabulate
from Encryption import EncryptionHelper
from ParserHelp import Parser
from DatabaseHelp import SQLQuery
import time
import datetime
from Main import User
from Exceptions import DBRecordError


class GP(User):
    """
    GP Class with navigation options and various functionalities.
    """

    def main_menu(self) -> None:
        """
        Main Menu for GP-type users.
        """
        while True:
            Parser.print_clean("You're currently viewing main menu options for GP {}.".format(self.username))
            option_selection = Parser.selection_parser(
                options={"A": "View/Edit availability", "M": "Manage bookings", "V": "View/Start appointment",
                         "--logout": "Logout"})

            Parser.print_clean("\n")
            if option_selection == "--logout":
                # Quitting is required for logout to ensure all personal data is cleared from session
                Parser.print_clean("Logging you out...")
                Parser.user_quit()

            elif option_selection == "A":
                self.edit_availability()
            elif option_selection == "M":
                self.manage_bookings()
            elif option_selection == "V":
                self.view_appointment()

    def edit_availability(self) -> None:
        """
        Method to view, add or remove availability for the logged in GP.
        """
        while True:
            Parser.print_clean()
            option_selection = Parser.selection_parser(
                options={"A": "View all your current availability", "D": "Edit availability by date",
                         "--back": "to go back"})
            if option_selection == "--back":
                Parser.print_clean("\n")
                return
            elif option_selection == "A":
                availability_result = SQLQuery("SELECT Timeslot FROM available_time WHERE StaffId = ?"
                                               ).executeFetchAll(parameters=(self.ID,))
                Parser.print_clean(f"Viewing current availability for GP {self.username}")
                if len(availability_result) == 0:
                    Parser.print_clean("You have no current availability recorded in the system.")
                else:
                    for slot in availability_result:
                        Parser.print_clean(slot[0])
                Parser.string_parser("Press Enter to continue...")
                continue
            selected_date = Parser.date_parser(f"Editing availability for GP {self.username}.\n"
                                               "Select a Date:")
            if selected_date == "--back":
                # --back returns the user to the main GP menu.
                Parser.print_clean()
                return
            Parser.print_clean()
            # Retrieving availability from the database
            availability_result = SQLQuery(
                "SELECT StaffID, Timeslot FROM available_time WHERE StaffID = ? AND Timeslot >= ? AND Timeslot <= ?",
            ).executeFetchAll(parameters=(self.ID, selected_date, selected_date + datetime.timedelta(days=1)))
            # Creating two corresponding tables for the fetched data - one for SQL manipulation, one for display
            availability_table_raw = []
            availability_table = []
            for i in range(len(availability_result)):
                availability_table.append([i + 1, str(availability_result[i][1])])
                availability_table_raw.append([i + 1, availability_result[i][1]])
            Parser.print_clean(f"You are viewing your schedule for: {selected_date}")
            options = {"A": "add availability"}
            if len(availability_table) == 0:
                Parser.print_clean(f"You have no availability for this day yet.\n")
            else:
                Parser.print_clean(tabulate(availability_table, headers=["Pointer", "Timeslot"]))
                options["R"] = "remove availability"

            options["--back"] = "back to previous page"
            option_selection = Parser.selection_parser(
                options=options)
            if option_selection == "A":
                # selected_date is passed as argument rather than an instance variable for safety
                # (selected_date is used as a variable name across many methods)
                self.add_availability(selected_date)
            elif (option_selection == "R") and (len(availability_table) >= 1):
                # the same applies to the availability table
                self.remove_availability(availability_table_raw)

    def remove_availability(self, availability_table) -> bool:
        """
        Method to remove available timeslots for a given day
        !IMPORTANT Should only be called from within GP.edit_availability
        
        :param: list availability_table: availability table for the selected day
        """
        slots_to_remove = []
        while True:
            # Selecting the entries to remove
            selected_entry = Parser.list_number_parser("Select the entry to remove using their corresponding IDs"
                                                       "from the 'Pointer' column.",
                                                       (1, len(availability_table) + 1))
            if selected_entry == '--back':
                return False
            for row in availability_table:
                if row[0] in selected_entry:
                    slots_to_remove.append(row[1])
            Parser.print_clean("These time slot will be removed and made unavailable for future bookings:")
            for slot in slots_to_remove:
                Parser.print_clean(slot)
            confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})
            # Confirm if user wants to delete slots
            if confirm == "Y":
                try:
                    for slot in slots_to_remove:
                        SQLQuery("DELETE FROM available_time WHERE StaffID = ? AND Timeslot = ?"
                                 ).executeCommit((self.ID, slot))
                    Parser.print_clean("Slots removed successfully.")
                    Parser.string_parser("Press Enter to continue...")
                    return True
                # temporary exception
                except DBRecordError:
                    Parser.print_clean("Error encountered")
                    slots_to_remove = []
                    Parser.string_parser("Press Enter to continue...")
            if confirm == "N":
                Parser.print_clean("Removal cancelled.")
                slots_to_remove = []
                Parser.string_parser("Press Enter to continue...")

    def add_availability(self, selected_date) -> bool:
        """
        Method to add availability for a given day
        !IMPORTANT Should only be called from within GP.edit_availability

        :param: datetime selected_date: Date for which availability is edited
        """
        stage = 0
        slots_to_add = []
        while True:
            while stage == 0:
                start_time = Parser.time_parser(f"GP {self.username}: you're adding availability for "
                                                f"{selected_date}. Each timeslot is 15 minutes long. \nEnter "
                                                f"the hour you wish to start taking appointments:")
                if start_time == "--back":
                    return False
                else:
                    selected_start = datetime.datetime.combine(selected_date, start_time)
                    stage = 1
            while stage == 1:
                end_time = Parser.time_parser(f"GP {self.username}: Each timeslot is  15 minutes long. You have "
                                              f"chosen to start from {str(selected_start)}. \nEnter the end"
                                              " of your last available appointment:")
                if end_time == "--back":
                    stage = 0
                else:
                    selected_end = datetime.datetime.combine(selected_date, end_time)
                    stage = 2
            while stage == 2:
                temporary_time = selected_start
                while temporary_time < selected_end:
                    slots_to_add.append(temporary_time)
                    temporary_time = temporary_time + datetime.timedelta(minutes=15)
                Parser.print_clean("You have chosen to add the following slots: ")
                for slot in slots_to_add:
                    Parser.print_clean(slot)
                confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})
                if confirm == "Y":
                    try:
                        for slot in slots_to_add:
                            SQLQuery("INSERT INTO available_time VALUES (?, ?)").executeCommit((self.ID, slot))
                        Parser.print_clean("Your slots have been successfully added!")
                        Parser.string_parser("Press Enter to continue...")
                        return True
                    # temporary exception
                    except DBRecordError:
                        Parser.print_clean("Invalid selection. Some of the entries may already be in the database. "
                                           "Please Retry")
                        stage = 0
                        slots_to_add = []
                        Parser.string_parser("Press Enter to continue...")
                if confirm == "N":
                    stage = 0
                    slots_to_add = []
                    Parser.print_clean("Starting over...")
                    time.sleep(2)

    def manage_bookings(self) -> None:
        """
        Method to manage bookings for a GP.
        """
        stage = 0
        while True:
            while stage == 0:
                Parser.print_clean(f"Managing bookings for GP {self.username}.")
                option_selection = Parser.selection_parser(
                    options={"P": "View and edit your pending bookings", "D": "View and edit bookings by date",
                             "--back": "to go back"})
                if option_selection == "--back":
                    Parser.print_clean("\n")
                    return
                elif option_selection == "P":
                    bookings_result = SQLQuery("SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, "
                                               "users.lastName, visit.Confirmed FROM visit INNER JOIN users ON "
                                               "visit.NHSNo = users.ID WHERE visit.StaffID = ? AND visit.Confirmed = "
                                               "'P'").executeFetchAll(EncryptionHelper(), parameters=(self.ID,))
                    message = "with status 'pending'."
                    stage = 1
                elif option_selection == "D":
                    selected_date = Parser.date_parser(question=f"Accessing bookings for GP {self.username}\n"
                                                                f"Select a Date:")
                    if selected_date == "--back":
                        return
                    else:
                        bookings_result = SQLQuery(
                            "SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, "
                            "users.lastName, visit.Confirmed FROM visit INNER JOIN users ON "
                            "visit.NHSNo = users.ID WHERE visit.StaffID = ? AND visit.Timeslot >= ?"
                            " AND visit.Timeslot <= ?"
                        ).executeFetchAll(EncryptionHelper(), (self.ID, selected_date,
                                                               selected_date + datetime.timedelta(
                                                                   days=1)))
                        message = f"for: {selected_date.strftime('%Y-%m-%d')}"
                        stage = 1
            while stage == 1:
                rows = GP.print_select_bookings(bookings_result, message)
                if not rows:
                    stage = 0
                else:
                    self.booking_transaction(rows[0], rows[1])

    @staticmethod
    def print_select_bookings(bookings_result, message):
        """
        :param list of tuples bookings_result: result of booking query
        :param message: message to GP
        :return: list of bookings, or False if no bookings are present in search criteria
        """
        bookings_table_raw = []
        bookings_table = []
        translation = {"T": "Accepted", "F": "Rejected", "P": "Pending Response"}
        i = 0
        for booking in bookings_result:
            bookings_table.append([i + 1, booking[0], str(booking[1]), booking[2], booking[3],
                                   booking[4], translation[booking[5]]])
            bookings_table_raw.append([i + 1, booking[0], booking[1]])
            i += 1
        Parser.print_clean("You are viewing your bookings " + message)
        if len(bookings_table) == 0:
            Parser.print_clean("No bookings match current search criteria.")
            # stage = 0
            Parser.string_parser("Press Enter to continue.")
            return False
        else:
            Parser.print_clean(tabulate(bookings_table,
                                        headers=["Pointer", "BookingNo", "timeslot", "Patient NHSNo", "P. First Name",
                                                 "P. Last Name", "Confirmed"]))
            selected_entry = Parser.integer_parser(question="Select entry using number from Pointer column or "
                                                            "type '--back' to go back")
            if selected_entry == "--back":
                return False
            else:
                selected_row = bookings_table[selected_entry - 1]
                selected_row_raw = bookings_table_raw[selected_entry - 1]
                return selected_row, selected_row_raw

    def booking_transaction(self, selected_row, selected_row_raw) -> bool:
        """
        Method to change the status of a given booking for a GP.
        !IMPORTANT Should only be called from within GP.manage_bookings

        :param: list selected_row: Row from database representing a given booking
        :param: list selected_row_raw: As above but in raw format (see GP.manage_bookings)
        """
        while True:
            Parser.print_clean("You selected the following booking:")
            Parser.print_clean(
                tabulate([selected_row], headers=["Pointer", "BookingNo", "timeslot", "Patient NHSNo", "P. First Name",
                                                  "P. Last Name", "Confirmed"]))
            user_input = Parser.selection_parser(
                options={"C": "Confirm", "R": "Reject", "--back": "Back to previous page"})
            if user_input == "--back":
                return False
            elif user_input == "C":
                Parser.print_clean("Warning! This will reject all other pending bookings for this timeslot. ")
                confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Rollback"})
                if confirm == 'N':
                    pass
                else:
                    SQLQuery("UPDATE Visit SET Confirmed = 'F' WHERE StaffID = ? AND Timeslot = ? AND BookingNo != ?"
                             ).executeCommit((self.ID, selected_row_raw[2], selected_row_raw[1]))
                    SQLQuery("UPDATE Visit SET Confirmed = 'T' WHERE BookingNo = ?"
                             ).executeCommit((selected_row_raw[1],))
                    return True
            elif user_input == "R":
                SQLQuery("UPDATE Visit SET Confirmed = 'F' WHERE BookingNo = ?").executeCommit((selected_row_raw[1],))
                return True

    def view_appointment(self):
        """
        step 1 in branch v ask which date the user wish to manipulate ->
        Display confirmed appointment of the date ->

        """
        stage = 0
        while True:
            while stage == 0:
                Parser.print_clean(f"Viewing confirmed appointments for GP {self.username}.")
                user_input = Parser.selection_parser(options={"T": "View today's appointments", "D": "Select by Date",
                                                              "--back": "to go back"})
                if user_input == "T":
                    selected_date = datetime.datetime.today().date()
                    Parser.print_clean(str(selected_date))
                    stage = 1
                elif user_input == "--back":
                    Parser.print_clean("\n")
                    return
                else:
                    selected_date = Parser.date_parser(question="Select a Date:")
                    if selected_date == "--back":
                        return
                    else:
                        stage = 1
            while stage == 1:
                bookings_result = SQLQuery("SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, "
                                           "users.lastName, visit.Confirmed FROM visit INNER JOIN users ON "
                                           "visit.NHSNo = users.ID WHERE visit.StaffID = ? AND visit.Timeslot >= ? AND "
                                           "visit.Timeslot <= ? AND visit.Confirmed = 'T' ").executeFetchAll(
                    decrypter=EncryptionHelper(),
                    parameters=(self.ID, selected_date, selected_date + datetime.timedelta(days=1)))
                message = f"for {selected_date.strftime('%Y-%m-%d')} (confirmed)."
                # booking_no = GP.print_select_bookings(bookings_result, message)[1][1]
                booking_no = GP.print_select_bookings(bookings_result, message)
                if not booking_no:
                    stage = 0
                else:
                    # GP.start_appointment(booking_no)
                    GP.start_appointment(booking_no[1][1])

    @staticmethod
    def start_appointment(booking_no):
        """
        step 2 in branch v
        show details of selected patient  ->
        ask the user whether they wish to change it ->
        for D and N they can change diagnosis or notes ->
        for P they can add or remove prescription
        """
        while True:
            booking_information = SQLQuery("SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, "
                                           "users.lastName, visit.Confirmed, users.birthday, users.phoneNo, "
                                           "users.HomeAddress, users.postcode, visit.diagnosis, visit.notes FROM visit "
                                           "INNER JOIN users ON visit.NHSNo = users.ID WHERE visit.BookingNo = ? "
                                           ).executeFetchAll(decrypter=EncryptionHelper(), parameters=(booking_no,))
            Parser.print_clean(tabulate([booking_information[0][:-3]],
                               headers=["BookingNo", "timeslot", "Patient NHSNo", "P. First Name", "P. Last Name",
                                        "Confirmed", "birthday", "phoneNo", "HomeAddress", "postcode"]))
            Parser.print_clean("\nDiagnosis:")
            Parser.print_clean(booking_information[0][10])
            Parser.print_clean("\n----------")
            Parser.print_clean("Notes:")
            Parser.print_clean(booking_information[0][11])
            Parser.print_clean("\n-------------")
            parser_result = SQLQuery("SELECT PrescriptionNumber, drugName, quantity, instructions FROM prescription "
                                     "WHERE BookingNo = ? "
                                     ).executeFetchAll(decrypter=EncryptionHelper(), parameters=(booking_no,))
            if parser_result:
                Parser.print_clean(tabulate(parser_result,
                                            headers=["Prescription No", "Drug Name", "Quantity",
                                                     "Dosage & Instructions"]))
            else:
                Parser.print_clean("Prescriptions:\nNone")

            Parser.print_clean("")
            user_input = Parser.selection_parser(
                options={"D": "Edit diagnosis", "N": "Add notes", "P": "Edit prescriptions",
                         "--back": "go back to previous page"})
            if user_input == "--back":
                return
            elif user_input == "D":
                Parser.print_clean(
                    f"The current diagnosis for patient {booking_information[0][3]} {booking_information[0][4]}, "
                    f"appointment number {booking_no}:")
                Parser.print_clean(booking_information[0][10])
                Parser.print_clean("")
                diagnosis = Parser.string_parser("Please enter your diagnosis: ")
                SQLQuery(" UPDATE Visit SET diagnosis = ? WHERE BookingNo = ? ").executeCommit((diagnosis, booking_no))
                Parser.print_clean("The diagnosis has been recorded successfully!")
                Parser.string_parser("Press Enter to continue...")

            elif user_input == "N":
                Parser.print_clean(f"Your notes for appointment number {booking_no}")
                Parser.print_clean("")
                Parser.print_clean(booking_information[0][11])
                notes_input = Parser.string_parser("Please enter your notes: ")
                SQLQuery(" UPDATE Visit SET notes = ? WHERE BookingNo = ? ").executeCommit((notes_input,
                                                                                            booking_no))
                Parser.print_clean("Your notes have been recorded successfully!")
                Parser.string_parser("Press Enter to continue...")

            elif user_input == "P":
                Parser.print_clean(f"Current prescription for patient {booking_information[0][3]} "
                                   f"{booking_information[0][4]} "
                                   f"under appointment number {booking_no}:")
                Parser.print_clean("")
                Parser.print_clean(tabulate(parser_result,
                                            headers=["Prescription No", "Drug Name", "Quantity", "Dosage & "
                                                                                                 "Instructions"]))
                Parser.print_clean("")
                user_input = Parser.selection_parser(
                    options={"A": "add prescription", "R": "remove prescription", "--back": "back to previous page"})
                if user_input == "--back":
                    continue
                elif user_input == "A":
                    drug_name = Parser.string_parser("Please enter the drug name: ")
                    quantity = Parser.integer_parser("Please enter the quantity: ")
                    instructions = Parser.string_parser("Please enter the instructions and dosage: ")
                    SQLQuery("INSERT INTO prescription (BookingNo, drugName, quantity, instructions) VALUES (?, ?, ?, "
                             "?)").executeCommit((booking_no, drug_name, quantity, instructions))
                    Parser.print_clean("Your prescription has been recorded successfully!")
                    Parser.string_parser("Press Enter to continue...")
                    continue
                elif user_input == "R":
                    while True:
                        allowed_numbers = [prescription[0] for prescription in parser_result]
                        prescription_number = str(Parser.integer_parser("Please enter the Prescription No to delete: "))
                        if prescription_number not in allowed_numbers:
                            Parser.print_clean("Incorrect prescription number!")
                            continue
                        SQLQuery(" DELETE FROM prescription WHERE PrescriptionNumber = ? "
                                 ).executeCommit((prescription_number,))
                        Parser.print_clean("Prescription removed correctly!")
                        Parser.string_parser("Press Enter to continue...")
                        break

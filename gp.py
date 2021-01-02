from tabulate import tabulate
from encryption import EncryptionHelper
from iohandler import Parser
from database import SQLQuery
import time
import datetime
from main import User, MenuHelper
from exceptions import DBRecordError

# logging
import logging
logger = logging.getLogger(__name__)


class GP(User):
    """
    GP Class with navigation options and various functionalities.
    """

    def main_menu(self) -> None:
        """
        Main Menu for GP-type users.
        """
        logger.info("logged in as GP")
        while True:
            print("You're currently viewing main menu options for GP {}.".format(self.username))
            option_selection = Parser.selection_parser(
                options={"A": "View/Edit availability", "M": "Manage bookings", "V": "View/Start appointment",
                         "--logout": "Logout"})

            if option_selection == "--logout":
                # Quitting is required for logout to ensure all personal data is cleared from session
                logger.info("User Logged Out")
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
                Parser.print_clean()
                return
            elif option_selection == "A":
                availability_result = SQLQuery("SELECT Timeslot FROM available_time WHERE StaffId = ?"
                                               ).fetch_all(parameters=(self.ID,))
                if len(availability_result) == 0:
                    print("You have no current availability recorded in the system.")
                else:
                    print(f"Viewing current availability for GP {self.username}")
                    for slot in availability_result:
                        print(slot[0])
                # input("Press Enter to continue...")
                Parser.handle_input()
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
            ).fetch_all(parameters=(self.ID, selected_date, selected_date + datetime.timedelta(days=1)))
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
                print(tabulate(availability_table, headers=["Pointer", "Timeslot"]))
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
            print("These time slot will be removed and made unavailable for future bookings:")
            for slot in slots_to_remove:
                print(slot)
            confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})
            # Confirm if user wants to delete slots
            if confirm == "Y":
                try:
                    for slot in slots_to_remove:
                        SQLQuery("DELETE FROM available_time WHERE StaffID = ? AND Timeslot = ?"
                                 ).commit((self.ID, slot))
                    print("Slots removed successfully.")
                    logger.info("Removed timeslot, DB transaction completed")
                    # input("Press Enter to continue...")
                    Parser.handle_input()
                    return True
                # temporary exception
                except DBRecordError:
                    print("Error encountered")
                    logger.warning("Error in DB, remove action failed")
                    slots_to_remove = []
                    # input("Press Enter to continue...")
                    Parser.handle_input()
            if confirm == "N":
                print("Removal cancelled.")
                slots_to_remove = []
                # input("Press Enter to continue...")
                Parser.handle_input()

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
                print("You have chosen to add the following slots: ")
                for slot in slots_to_add:
                    print(slot)
                confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})
                if confirm == "Y":
                    try:
                        for slot in slots_to_add:
                            SQLQuery("INSERT INTO available_time VALUES (?, ?)").commit((self.ID, slot))
                        print("Your slots have been successfully added!")
                        logger.info("Added timeslot, DB transaction completed")
                        # input("Press Enter to continue...")
                        Parser.handle_input()
                        return True
                    # temporary exception
                    except DBRecordError:
                        print("Invalid selection. Some of the entries may already be in the database. "
                              "Please Retry")
                        stage = 0
                        slots_to_add = []
                        logger.warning("Error in DB, add action failed")
                        Parser.string_parser("Press Enter to continue...")
                if confirm == "N":
                    stage = 0
                    slots_to_add = []
                    print("Starting over...")
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
                    Parser.print_clean()
                    return
                elif option_selection == "P":
                    bookings_result = SQLQuery("SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, "
                                               "users.lastName, visit.Confirmed FROM visit INNER JOIN users ON "
                                               "visit.NHSNo = users.ID WHERE visit.StaffID = ? AND visit.Confirmed = "
                                               "'P'").fetch_all(EncryptionHelper(), parameters=(self.ID,))
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
                        ).fetch_all(EncryptionHelper(), (self.ID, selected_date,
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
        print("You are viewing your bookings " + message)
        if len(bookings_table) == 0:
            print("No bookings match current search criteria.")
            # stage = 0
            # input("Press Enter to continue.")
            Parser.handle_input()
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
            print("You selected the following booking:")
            print(
                tabulate([selected_row], headers=["Pointer", "BookingNo", "timeslot", "Patient NHSNo", "P. First Name",
                                                  "P. Last Name", "Confirmed"]))
            user_input = Parser.selection_parser(
                options={"C": "Confirm", "R": "Reject", "--back": "Back to previous page"})
            if user_input == "--back":
                return False
            elif user_input == "C":
                print("Warning! This will reject all other pending bookings for this timeslot. ")
                confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Rollback"})
                if confirm == 'N':
                    pass
                else:
                    SQLQuery("UPDATE Visit SET Confirmed = 'F' WHERE StaffID = ? AND Timeslot = ? AND BookingNo != ?"
                             ).commit((self.ID, selected_row_raw[2], selected_row_raw[1]))
                    logger.info("removing conflicting confirmed bookings")
                    SQLQuery("UPDATE Visit SET Confirmed = 'T' WHERE BookingNo = ?"
                             ).commit((selected_row_raw[1],))
                    logger.info("setting selected booking as confirmed, action successful")
                    return True
            elif user_input == "R":
                SQLQuery("UPDATE Visit SET Confirmed = 'F' WHERE BookingNo = ?").commit((selected_row_raw[1],))
                logger.info("removing confirmed bookings")
                return True

    def view_appointment(self):
        """
        step 1 in branch v ask which date the user wish to manipulate ->
        Display confirmed appointment of the date ->
        """
        stage = 0
        while True:
            Parser.print_clean()
            while stage == 0:
                print(f"Viewing confirmed appointments for GP {self.username}.")
                user_input = Parser.selection_parser(options={"T": "View today's appointments", "D": "Select by Date",
                                                              "--back": "to go back"})
                if user_input == "T":
                    selected_date = datetime.datetime.today().date()
                    print(str(selected_date))
                    stage = 1
                elif user_input == "--back":
                    print("\n")
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
                                           "visit.Timeslot <= ? AND visit.Confirmed = 'T' ").fetch_all(
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
        logger.info(f"starting appointment on bookingNo: {booking_no}")
        # starting encrypter
        encrypter = EncryptionHelper()
        while True:
            booking_information = SQLQuery("SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, "
                                           "users.lastName, visit.Confirmed, users.birthday, users.phoneNo, "
                                           "users.HomeAddress, users.postcode, visit.diagnosis, visit.notes FROM visit "
                                           "INNER JOIN users ON visit.NHSNo = users.ID WHERE visit.BookingNo = ? "
                                           ).fetch_all(decrypter=EncryptionHelper(), parameters=(booking_no,))
            print(tabulate([booking_information[0][:-3]],
                           headers=["BookingNo", "timeslot", "Patient NHSNo", "P. First Name", "P. Last Name",
                                    "Confirmed", "birthday", "phoneNo", "HomeAddress", "postcode"]))
            print("\nDiagnosis:")
            print(booking_information[0][10])
            print("\n----------")
            print("Notes:")
            print(booking_information[0][11])
            print("\n-------------")
            parser_result = SQLQuery("SELECT PrescriptionNumber, drugName, quantity, instructions FROM prescription "
                                     "WHERE BookingNo = ? "
                                     ).fetch_all(decrypter=EncryptionHelper(), parameters=(booking_no,))
            if parser_result:
                print(tabulate(parser_result,
                               headers=["Prescription No", "Drug Name", "Quantity",
                                        "Dosage & Instructions"]))
            else:
                print("Prescriptions:\nNone")

            # Parser.print_clean() #this one seems to be wrong
            user_input = Parser.selection_parser(
                options={"D": "Edit diagnosis", "N": "Add notes", "P": "Edit prescriptions",
                         "--back": "go back to previous page"})
            if user_input == "--back":
                return
            elif user_input == "D":
                print(
                    f"The current diagnosis for patient {booking_information[0][3]} {booking_information[0][4]}, "
                    f"appointment number {booking_no}:")
                print(booking_information[0][10])
                print("")
                diagnosis = Parser.string_parser("Please enter your diagnosis: ")
                diagnosis_encrypted = encrypter.encrypt_to_bits(info=diagnosis)
                SQLQuery(" UPDATE Visit SET diagnosis = ? WHERE BookingNo = ? ").commit(
                    (diagnosis_encrypted, booking_no))
                logger.info(f"Updated diagnosis for booking: {booking_no}")
                print("The diagnosis has been recorded successfully!")
                # input("Press Enter to continue...")
                Parser.handle_input()

            elif user_input == "N":
                print(f"Your notes for appointment number {booking_no}")
                print("")
                print(booking_information[0][11])
                notes_input = Parser.string_parser("Please enter your notes: ")
                notes_input_encrypted = encrypter.encrypt_to_bits(info=notes_input)
                SQLQuery(" UPDATE Visit SET notes = ? WHERE BookingNo = ? ").commit((notes_input_encrypted,
                                                                                     booking_no))
                logger.info(f"Updated Notes for booking: {booking_no}")
                print("Your notes have been recorded successfully!")
                # input("Press Enter to continue...")
                Parser.handle_input()

            elif user_input == "P":
                print(f"Current prescription for patient {booking_information[0][3]} "
                      f"{booking_information[0][4]} "
                      f"under appointment number {booking_no}:")
                print("")
                print(tabulate(parser_result,
                               headers=["Prescription No", "Drug Name", "Quantity", "Dosage & "
                                                                                    "Instructions"]))
                print("")
                user_input = Parser.selection_parser(
                    options={"A": "add prescription", "R": "remove prescription", "--back": "back to previous page"})
                if user_input == "--back":
                    continue
                elif user_input == "A":
                    drug_name = Parser.string_parser("Please enter the drug name: ")
                    quantity = str(Parser.integer_parser("Please enter the quantity: "))
                    instructions = Parser.string_parser("Please enter the instructions and dosage: ")
                    drug_name_encrypted = encrypter.encrypt_to_bits(info=drug_name)
                    quantity_encrypted = encrypter.encrypt_to_bits(info=quantity)
                    instructions_encrypted = encrypter.encrypt_to_bits(info=instructions)
                    SQLQuery("INSERT INTO prescription (BookingNo, drugName, quantity, instructions) VALUES (?, ?, ?, "
                             "?)").commit(
                        (booking_no, drug_name_encrypted, quantity_encrypted, instructions_encrypted))
                    logger.info(f"Drug: {drug_name} for current patient added to DB successfully")
                    Parser.print_clean("Your prescription has been recorded successfully!")
                    # input("Press Enter to continue...")
                    Parser.handle_input()
                    continue
                elif user_input == "R":
                    while True:
                        allowed_numbers = [prescription[0] for prescription in parser_result]
                        prescription_number = Parser.integer_parser("Please enter the Prescription No to delete: ")

                        if prescription_number not in allowed_numbers:
                            print("Incorrect prescription number!")
                            continue
                        SQLQuery("DELETE FROM prescription WHERE PrescriptionNumber = ?"
                                 ).commit((prescription_number,))
                        print("Prescription removed correctly!")
                        logger.info(f"PrescriptionNo: {prescription_number} removed from DB successfully")
                        # input("Press Enter to continue...")
                        Parser.handle_input()
                        break

    def first_login(self):
        Parser.print_clean("Welcome GP {}. This is your first login. ".format(self.username))
        print("You need to input additional information before you can proceed.")
        Parser.handle_input("Press Enter to continue...")
        encrypt = EncryptionHelper().encrypt_to_bits
        specialty = encrypt(Parser.string_parser("Enter your specialisation: "))
        Parser.print_clean("Enter your gender: ")
        gender = Parser.selection_parser(options={"M": "Male", "F": "Female", "N": "Do not disclose"})
        clinic_address = encrypt(Parser.string_parser("Enter your clinic address (one line): "))
        clinic_postcode = MenuHelper.valid_postcode()
        info = encrypt(Parser.string_parser("Enter an intro paragraph about yourself: "))
        try:
            SQLQuery("INSERT INTO GP(ID, Gender, ClinicAddress, ClinicPostcode, Speciality, Introduction) VALUES (?, "
                     "?, ?, ?, ?, ?)").commit(parameters=(self.ID, gender, clinic_address, clinic_postcode,
                                                          specialty, info))
            return True
        except Exception as e:
            print(e)
            print("Database error")
            return False

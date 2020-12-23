import os
from tabulate import tabulate

from encryption import encryptionHelper
from parser_help import Parser
from database_help import SQLQuery
import time
# import sys
import datetime
from main import User

print_clean = Parser.print_clean
delta = datetime.timedelta


class GP(User):
    """
    GP Class with navigation options and various functionalities.
    """

    def main_menu(self) -> None:
        """
        Main Menu for GP-type users.
        """
        while True:
            print("You're currently viewing main menu options for GP {}.".format(self.username))
            option_selection = Parser.selection_parser(
                options={"A": "View/Edit availability", "M": "Manage bookings", "V": "View/Start appointment",
                         "--logout": "Logout"})
            if option_selection == "--logout":
                # Quitting is required for logout to ensure all personal data is cleared from session
                print_clean("Logging you out...")
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
            print_clean()
            option_selection = Parser.selection_parser(
                options={"A": "View all your current availability", "D": "Edit availability by date", "--back":
                    "to go back"})
            if option_selection == "--back":
                return
            elif option_selection == "A":
                availability_result = SQLQuery("SELECT Timeslot FROM available_time WHERE StaffId = ?"
                                               ).executeFetchAll(parameters=(self.ID,))
                print_clean(f"Viewing current availability for GP {self.username}")
                if len(availability_result) == 0:
                    print("You have no current availability recorded in the system.")
                else:
                    for slot in availability_result:
                        print(slot[0])
                input("Press Enter to continue...")
                continue
            selected_date = Parser.date_parser(f"Editing availability for GP {self.username}.\n"
                                               "Select a Date:")
            if selected_date == "--back":
                # --back returns the user to the main GP menu.
                print_clean()
                return
            print_clean()
            # Retrieving availability from the database
            availability_result = SQLQuery(
                "SELECT StaffID, Timeslot FROM available_time WHERE StaffID = ? AND Timeslot >= ? AND Timeslot <= ?",
            ).executeFetchAll(parameters=(self.ID, selected_date, selected_date + delta(days=1)))
            # Creating two corresponding tables for the fetched data - one for SQL manipulation, one for display
            availability_table_raw = []
            availability_table = []
            for i in range(len(availability_result)):
                availability_table.append([i + 1, str(availability_result[i][1])])
                availability_table_raw.append([i + 1, availability_result[i][1]])
            print(f"You are viewing your schedule for: {selected_date}")
            if len(availability_table) == 0:
                print(f"You have no availability for this day yet.")
            else:
                print(tabulate(availability_table, headers=["Pointer", "Timeslot"]))
            option_selection = Parser.selection_parser(
                options={"A": "add availability", "R": "remove availability", "--back": "back to previous page"})
            if option_selection == "A":
                # selected_date is passed as argument rather than an instance variable for safety
                # (selected_date is used as a variable name across many methods)
                self.add_availability(selected_date)
            elif option_selection == "R":
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
                                 ).executeCommit((self.ID, slot))
                    print("Slots removed successfully.")
                    input("Press Enter to continue...")
                    return True
                except:
                    print("Error encountered")
                    slots_to_remove = []
                    input("Press Enter to continue...")
            if confirm == "N":
                print("Removal cancelled.")
                slots_to_remove = []
                input("Press Enter to continue...")

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
                    temporary_time = temporary_time + delta(minutes=15)
                print("You have chosen to add the following slots: ")
                for slot in slots_to_add:
                    print(slot)
                confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})
                if confirm == "Y":
                    try:
                        for slot in slots_to_add:
                            SQLQuery("INSERT INTO available_time VALUES (?, ?)").executeCommit((self.ID, slot))
                        print("Your slots have been successfully added!")
                        input("Press Enter to continue...")
                        return True
                    except:
                        print("Invalid selection. Some of the entries may already be in the database. Please Retry")
                        stage = 0
                        slots_to_add = []
                        input("Press Enter to continue...")
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
                print_clean(f"Managing bookings for GP {self.username}.")
                option_selection = Parser.selection_parser(
                    options={"P": "View and edit your pending bookings", "D": "View and edit bookings by date",
                             "--back": "to go back"})
                if option_selection == "--back":
                    return
                elif option_selection == "P":
                    bookings_result = SQLQuery("SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, "
                                               "users.lastName, visit.Confirmed FROM visit INNER JOIN users ON "
                                               "visit.NHSNo = users.ID WHERE visit.StaffID = ? AND visit.Confirmed = "
                                               "'P'").executeFetchAll(encryptionHelper(), parameters=(self.ID,))
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
                        ).executeFetchAll(encryptionHelper(), (self.ID, selected_date,
                                                               selected_date + delta(
                                                                   days=1)))
                        message = f"for: {selected_date.strftime('%Y-%m-%d')}"
                        stage = 1
            while stage == 1:
                bookings_table_raw = []
                bookings_table = []
                translation = {"T": "Accepted", "F": "Rejected", "P": "Pending Response"}
                i = 0
                for booking in bookings_result:
                    bookings_table.append([i + 1, booking[0], str(booking[1]), booking[2], booking[3],
                                           booking[4], translation[booking[5]]])
                    bookings_table_raw.append([i + 1, booking[0], booking[1]])
                    i += 1
                print_clean("You are viewing your bookings " + message )
                if len(bookings_table) == 0:
                    print("No bookings match current search criteria.")
                    stage = 0
                    input("Press Enter to continue.")
                else:
                    print(tabulate(bookings_table,
                                   headers=["Pointer", "BookingNo", "timeslot", "Patient NHSNo", "P. First Name",
                                            "P. Last Name", "Confirmed"]))
                    selected_entry = Parser.integer_parser(question="Select entry using number from Pointer column or "
                                                                    "type '--back' to go back")
                    if selected_entry == "--back":
                        stage = 0
                    else:
                        selected_row = bookings_table[selected_entry - 1]
                        selected_row_raw = bookings_table_raw[selected_entry - 1]
                        self.booking_transaction(selected_row, selected_row_raw)

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
                             ).executeCommit((self.ID, selected_row_raw[2], selected_row_raw[1]))
                    SQLQuery("UPDATE Visit SET Confirmed = 'T' WHERE BookingNo = ?"
                             ).executeCommit((selected_row_raw[1],))
                    return True
            elif user_input == "R":
                SQLQuery("UPDATE Visit SET Confirmed = 'F' WHERE BookingNo = ?").executeCommit((selected_row_raw[1],))
                return True

    def view_appointment(self):
        """
        step 1 in branch v ask which date the user wish to manipulte ->
        Display confirmed appointment of the date ->

        """
        stage = 0
        selectedDate = None
        while True:
            while stage == 0:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                dateInput = Parser.date_parser(question="Select a Date:")
                if dateInput == "--back":
                    return "main"
                else:
                    selectedDate = dateInput
                    stage = 1
            while stage == 1:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                Qtext = "SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, users.lastName, visit.Confirmed "
                Qtext += "FROM visit INNER JOIN users ON visit.NHSNo = users.ID "
                Qtext += "WHERE visit.StaffID = ? AND visit.Timeslot >= ? AND visit.Timeslot <= ? AND visit.Confirmed = 'T' "
                # print(Qtext)
                Qbooked = SQLQuery(Qtext)

                selectedDatePlus1 = selectedDate + datetime.timedelta(days=1)
                Qbookedresult = Qbooked.executeFetchAll(decrypter=user.encryptionKey,
                                                        parameters=(user.ID, selectedDate, selectedDatePlus1))
                QbookedTableRaw = []
                QbookedTable = []
                translation = {"T": "Accepted", "F": "Rejected", "P": "Pending Response"}
                for i in range(len(Qbookedresult)):
                    QbookedTable.append(
                        [i + 1, Qbookedresult[i][0], str(Qbookedresult[i][1]), Qbookedresult[i][2], Qbookedresult[i][3],
                         Qbookedresult[i][4], translation[Qbookedresult[i][5]]])
                    QbookedTableRaw.append([i + 1, Qbookedresult[i][0], Qbookedresult[i][2]])
                print(f"You are viewing all of your confirmed bookings of: {selectedDate.strftime('%Y-%m-%d')}")
                print(tabulate(QbookedTable,
                               headers=["Pointer", "BookingNo", "timeslot", "Patient NHSNo", "P. First Name",
                                        "P. Last Name", "Confirmed"]))
                # print(tabulate(QbookedTableRaw, headers=["Pointer", "BookingNo", "Patient NHSNo"]))
                selectEntryNo = Parser.integer_parser(question="Select Entry using number or input '--back' for back")
                print(selectEntryNo)
                if selectEntryNo == "--back":
                    stage = 0
                    break
                # selectedRow = QbookedTable[selectEntryNo-1]
                # print(selectedRow)
                # selectedNhsNo = QbookedTableRaw[selectEntryNo-1][2]
                # print(selectedNhsNo)

                selectedBookingNo = QbookedTableRaw[selectEntryNo - 1][1]
                print(selectedBookingNo)

                GP.chooseAppointment(selectedBookingNo, user)

    @staticmethod
    def chooseAppointment(selectedBookingNo, user):
        """
        step 2 in branch v
        show details of selected patient  ->
        ask the user whether they wish to change it ->
        for D and N they can change diagnosis or notes ->
        for P they can add or remove prescription
        """

        while True:

            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            Qtext = "SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, users.lastName, visit.Confirmed, users.birthday, users.phoneNo, users.HomeAddress, users.postcode, visit.diagnosis, visit.notes "
            Qtext += "FROM visit INNER JOIN users ON visit.NHSNo = users.ID "
            Qtext += "WHERE visit.BookingNo = ? "
            Qbooked = SQLQuery(Qtext)
            Qbookedresult = Qbooked.executeFetchAll(decrypter=user.encryptionKey, parameters=(selectedBookingNo,))
            print(tabulate([Qbookedresult[0][:-3]],
                           headers=["BookingNo", "timeslot", "Patient NHSNo", "P. First Name", "P. Last Name",
                                    "Confirmed", "birthday", "phoneNo", "HomeAddress", "postcode"]))
            print("----------")
            print("Diagnosis:")
            print("----------")
            print(Qbookedresult[0][10])
            print("----------")
            print("Notes:")
            print("----------")
            print(Qbookedresult[0][11])
            print("-------------")
            print("Prescription:")
            print("-------------")
            Qtext = "SELECT drugName, quantity, instructions "
            Qtext += "FROM prescription WHERE BookingNo = ? "
            Qprescription = SQLQuery(Qtext)
            Qprescriptionresult = Qprescription.executeFetchAll(decrypter=user.encryptionKey,
                                                                parameters=(selectedBookingNo,))
            QprescriptionresultTable = []
            for i in range(len(Qprescriptionresult)):
                QprescriptionresultTable.append(
                    [i + 1, Qprescriptionresult[i][0], Qprescriptionresult[i][1], Qprescriptionresult[i][2]])
            print(tabulate(QprescriptionresultTable, headers=["ItemNo", "Drug Name", "Qanntity", "Instrctions"]))
            print("--------------")
            userInput = Parser.selectionParser(
                options={"D": "add diagnosis", "N": "add notes", "P": " edit prescription",
                         "--back": "back to previous page"})
            if userInput == "--back":
                return
            elif userInput == "D":
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print(f"Here is your diagnosis for Booking Number {Qbookedresult[0][0]}")
                print("----------")
                print("Diagnosis:")
                print("----------")
                print(Qbookedresult[0][10])
                QuerryDiagnosis = SQLQuery(" UPDATE Visit SET diagnosis = ? WHERE BookingNo = ? ")

                diagnosisInput = Parser.stringParser("Please enter your diagnosis:")

                exeQuerryDiagnosis = QuerryDiagnosis.executeCommit((diagnosisInput, Qbookedresult[0][0]))
                print("Your diagnosis has been given, you are going back to the patient info page...")

            elif userInput == "N":
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print(f"Here is your note for Booking Number {Qbookedresult[0][0]}")
                print("----------")
                print("Notes:")
                print("----------")
                print(Qbookedresult[0][11])
                QuerryDiagnosis = SQLQuery(" UPDATE Visit SET notes = ? WHERE NHSNo = ? ")
                # notesInput = input("Please enter your notes:\n")
                notesInput = Parser.stringParser("Please enter your notes:")
                # print(notesInput)
                exeQuerryNotes = QuerryDiagnosis.executeCommit((notesInput, Qbookedresult[0][0]))
                print("Your notes has been given,you are going back to the patient info page...")

            elif userInput == "P":
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print(f"Here is your Prescription for Booking Number {Qbookedresult[0][0]}")
                print("-------------")
                print("Prescription:")
                print("-------------")
                print(tabulate(QprescriptionresultTable, headers=["ItemNo", "Drug Name", "Qanntity", "Instrctions"]))

                userInput = Parser.selectionParser(
                    options={"A": "add prescription", "R": "remove prescription", "--back": "back to previous page"})
                if userInput == "--back":
                    return
                elif userInput == "A":
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                    Querryprescription = SQLQuery(
                        " INSERT INTO prescription (BookingNo, drugName, quantity, instructions) VALUES (?, ?, ?, ?)  ")
                    # BookingNo = input("Please enter your BookingNo:\n")
                    # print(notesInput)
                    # drugName = input("Please enter your drugName:\n")
                    drugName = Parser.stringParser("Please enter your drugname:")
                    # quantity = input("Please enter your quantity:\n")
                    quantity = Parser.stringParser("Please enter your quantity:")
                    # instructions = input("Please enter your instructions:\n")
                    instructions = Parser.stringParser("Please enter your instructions:")

                    exeQuerryprescription = Querryprescription.executeCommit(
                        (Qbookedresult[0][0], drugName, quantity, instructions))
                    print("Your prescription has been given,you are going back to the patient info page...")

                elif userInput == "R":
                    GP.removePrescripion(Qbookedresult[0][0], QprescriptionresultTable)

    @staticmethod
    def removePrescripion(BookingNo, QprescriptionresultTable):
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print(f"Here is your Prescription for Booking Number {BookingNo}")
        print("-------------")
        print("Prescription:")
        print("-------------")
        print(tabulate(QprescriptionresultTable, headers=["ItemNo", "Drug Name", "Qanntity", "Instrctions"]))
        Querryprescription = SQLQuery(" DELETE FROM prescription WHERE BookingNo = ? AND drugName = ? ")
        selectItemNo = Parser.integer_parser(question="Select Item using number")
        if selectItemNo == "--back":
            return
        # print(notesInput)
        exeQuerryprescription = Querryprescription.executeCommit(
            (BookingNo, QprescriptionresultTable[selectItemNo - 1][1]))
        print("this prescription has been removed,you are going back to the patient info page...")
        return

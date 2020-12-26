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


class Patient(User):
    """
    GP Class with navigation options and various functionalities.
    """

    def main_menu(self) -> None:
        """
        Main Menu for GP-type users.
        """
        while True:
            print("You're currently viewing main menu options for Patient {}.".format(self.username))
            option_selection = Parser.selection_parser(
                options={"B": "book appointments", "C": "cancel appiontment", "R": "review appointments",
                         "--logout": "Logout"})
            if option_selection == "--logout":
                # Quitting is required for logout to ensure all personal data is cleared from session
                print_clean("Logging you out...")
                Parser.user_quit()

            elif option_selection == "B":
                self.book_appointment()
            elif option_selection == "C":
                self.cancel_appointment()
            elif option_selection == "R":
                self.review_appointment()


    def book_appointment(self):
        selected_date = Parser.date_parser(f"Book appointments for patient {self.username}.\n"
                                           "Select a Date:")
        if selected_date == "--back":
            # --back returns the user to the main GP menu.
            print_clean()
            return
        print_clean()
        # Retrieving availability from the database
        availabelbooking_result = SQLQuery(
            "SELECT StaffID, Timeslot FROM available_time WHERE Timeslot >= ? AND Timeslot <= ?",
        ).executeFetchAll(parameters=(selected_date, selected_date + delta(days=1)))
        # Creating two corresponding tables for the fetched data - one for SQL manipulation, one for display
        availability_table_raw = []
        availability_table = []
        for i in range(len(availabelbooking_result)):
            availability_table.append([i + 1, str(availabelbooking_result[i][1])])
            availability_table_raw.append([i + 1, availabelbooking_result[i][1]])
        print(f"There are available appointments for: {selected_date}")
        if len(availability_table) == 0:
            print(f"There is no appointment for this day yet.")
        else:
            print(tabulate(availability_table, headers=["Pointer", "Timeslot"]))
        option_selection = Parser.selection_parser(
            options={"B": "Book appointments",  "--back": "back to previous page"})
        if option_selection == "--back":
            return
        else:

            desccription = MenuHelper.getIllness()

        @staticmethod
        def getIllness():
            return EncryptionHelper().encryptToBits(Parser.string_parser("Please enter your description of illness:"))


            insert_query = SQLQuery("Insert INTO  VALUES ()")
        pass



    def cancel_appointment(self):
        pass

    def review_appointment(self):
        pass
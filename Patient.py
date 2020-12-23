import os
from tabulate import tabulate

import getpass
from encryption import encryptionHelper, passwordHelper
from login import currentUser, loginHelp
from parserHelp import parser
from databaseHelp import SQLQuerry
import time
import sys

class PatientNavigator:
    """Class patient and attributes."""
    def PatientNavigator(self, patient_user):
        """
        print the user information
        """
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print(f"Login Successful. Hello {patient_user.firstName}")
        user_info_table = [("User Type:", patient_user.UserType),
                           ("First Name: ", patient_user.firstName),
                           ("Last Name: ", patient_user.lastName),
                           ("Birthday: ", patient_user.birthday),
                           ("Phone No: ", patient_user.phoneNo),
                           ("Home Address: ", patient_user.HomeAddress),
                           ("Post Code: ", patient_user.postCode)]
        print(tabulate(user_info_table))


        while True:
            user_input = parser.selectionParser(
                options={"A": "Book Appointments", "B": "Cancel Appointments", "C": "Edit Appointmens",
                         "D": "Review Appointments", "--logout": "logout"})
            if user_input == "--logout":
                # reason for quitting is that it dumps the login info so the logout is complete and the key is not
                # accessible to future user.
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Logging you out ...")
                time.sleep(3)
                sys.exit(0)
            else:
                current_page = user_input

            if current_page == "A":
                # PatientNavigator().bookApmt()
                self.bookApmt()
            elif current_page == "B":
                self.cancelApmt()
            elif current_page == "C":
                self.editApmt()
            else:
                self.reviewApmt()

    @staticmethod
    def reviewApmt():
        pass

    def bookApmt(self):
        pass

    def cancelApmt(self):
        pass

    def editApmt(self):
        pass
        
import os
from tabulate import tabulate
from Main import User, MenuHelper

from Encryption import EncryptionHelper, PasswordHelper
from parserHelp import parser
from DatabaseHelp import SQLQuery
import time
import sys

from parser_help import Parser


class Patient(User):
    """Navigate through Patient features."""

    def PatientNavigator(self):
        """
        Main Menu for Patient-type users.
        """
        while True:
            user_input = parser.selectionParser(
                options={"A": "Book Appointments", "B": "Cancel Appointments", "C": "Edit Appointments",
                         "D": "Review Appointments", "--logout": "logout"})
            if user_input == "--logout":
                Parser.user_quit()

            if user_input == "A":
                self.bookApmt()
            elif user_input == "B":
                self.cancelApmt()
            elif user_input == "C":
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


if __name__ == "__main__":
    current_user = MenuHelper.login()
    MenuHelper.dispatcher(current_user["username"], current_user["user_type"])
    Patient(current_user).main_menu()

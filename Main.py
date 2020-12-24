"""Main Program here."""
from parser_help import Parser
import time
from DatabaseHelp import SQLQuery
from Encryption import EncryptionHelper
from Encryption import PasswordHelper
import sys
import os
from getpass import getpass
from tabulate import tabulate

from Exceptions import *


class MenuHelper:
    """
    Helper class for initialising the main menu.
    Methods for login, registering and starting specific sub-functionalities
    """
    @staticmethod
    def login():
        for i in range(4, -1, -1):
            # limit to 5 username attempts
            try:
                # trying to get username
                try_username = Parser.string_parser("Please enter your username: ")
                # retrieving the user if exist to compare to PW
                username_query = SQLQuery("SELECT username, passCode, Deactivated, UserType FROM Users "
                                          "WHERE username == ?")
                query_result = username_query.executeFetchAll(parameters=(try_username,))
                if len(query_result) != 1:
                    raise DBRecordError
                else:
                    username = try_username
                    login_array = query_result[0]
                    user_type = login_array[3]
                    print("Username validated.")
                    break
            except DBRecordError:
                print(f"Invalid Username: {i} attempts remaining")
        else:
            print("You've entered an incorrect username too many times.")
            Parser.user_quit()
        for i in range(4, -1, -1):
            try:
                # the PW is saved in hash so need to convert to hash to compare special parsing function because it will
                # hide the needed
                try_pw = PasswordHelper.hashPW(getpass("Enter your password: "))
                if try_pw == login_array[1]:
                    print("Password correct!")
                    if login_array[2] == "T":
                        print("Your account is deactivated. Please contact the system administrator. ")
                        Parser.user_quit()
                    else:
                        return {"username": username, "user_type": user_type}
                else:
                    raise DBRecordError
            except DBRecordError:
                print(f"Invalid Password: {i} attempts remaining")
        else:
            print("You've entered an incorrect password too many times.")
            Parser.user_quit()

    @staticmethod
    def dispatcher(username, user_type):
        if user_type == "Admin":
            from Admin import Admin
            user = Admin(username)
        elif user_type == "GP":
            from GP import GP
            user = GP(username)
        else:
            from Patient import Patient
            user = Patient(username)

        user.print_hello()
        user.print_information()
        user.main_menu()


class User:
    def __init__(self, username):
        """
        initializing user login process and return a currentUser Object
        """
        self.username = username

        # retrieving the full information from DATAbase instead of just the password for authentication
        self.user_data = SQLQuery(
            "SELECT ID, username, firstName, lastName, phoneNo, HomeAddress, postCode, UserType, "
            "deactivated, birthday FROM Users WHERE username == ?").executeFetchAll(decrypter=EncryptionHelper(),
                                                                                    parameters=(username,))[0]
        # loading the user info into a state
        self.ID = self.user_data[0]
        self.username = self.user_data[1]
        self.first_name = self.user_data[2]
        self.last_name = self.user_data[3]
        self.phone_no = self.user_data[4]
        self.home_address = self.user_data[5]
        self.postcode = self.user_data[6]
        self.user_type = self.user_data[7]
        self.deactivated = self.user_data[8]
        self.birthday = self.user_data[9]

    def print_hello(self):
        Parser.print_clean(f"Login Successful. Hello {self.first_name}")
        return True

    def print_information(self):
        print(tabulate([("User Type:", self.user_type),
                        ("First Name: ", self.first_name),
                        ("Last Name: ", self.last_name),
                        ("Birthday: ", self.birthday),
                        ("Phone No: ", self.phone_no),
                        ("Home Address: ", self.home_address),
                        ("Post Code: ", self.postcode)
                        ]))
        return True


if __name__ == '__main__':
    # Exception handling if database not present/cannot connect
    # conn = create_connection("GPDB.db")

    while True:
        print("Welcome to Group 6 GP System")
        option_selection = Parser.selection_parser(options={"R": "register", "L": "login", "--quit": "quit"})

        if option_selection == 'L':
            current_user = MenuHelper.login()
            MenuHelper.dispatcher(current_user["username"], current_user["user_type"])

        elif option_selection == 'R':
            # not done
            print("register")
            quit()

import sqlite3

from parser_help import Parser
from database_help import SQLQuery
from encryption import EncryptionHelper
from encryption import PasswordHelper
from getpass import getpass
from tabulate import tabulate
from exceptions import DBRecordError, InValidPhoneNumberError, \
    InValidPostcodeError, InValidUsernameError, InValidPasswordError


class MenuHelper:
    """
    Helper class for initialising the main menu.
    Methods for login, registering and starting specific sub-functionalities
    """
    @staticmethod
    def login():
        """
        Login to a registered account.
        """
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
                    Parser.print_clean("Username validated.")
                    break
            except DBRecordError:
                Parser.print_clean(f"Invalid Username: {i} attempts remaining")
        else:
            Parser.print_clean("You've entered an incorrect username too many times.")
            Parser.user_quit()
        for i in range(4, -1, -1):
            try:
                # the PW is saved in hash so need to convert to hash to compare special parsing function because it will
                # hide the needed
                try_pw = PasswordHelper.hashPW(getpass("Enter your password: "))
                if try_pw == login_array[1]:
                    Parser.print_clean("Password correct!")
                    if login_array[2] == "T":
                        Parser.print_clean("Your account is deactivated. Please contact the system administrator. ")
                        Parser.user_quit()
                    else:
                        return {"username": username, "user_type": user_type}
                else:
                    raise DBRecordError
            except DBRecordError:
                Parser.print_clean(f"Invalid Password: {i} attempts remaining")
        else:
            Parser.print_clean("You've entered an incorrect password too many times.")
            Parser.user_quit()

    @staticmethod
    def register():
        """
        Register a new GP or Patient Account.
        """
        new_id, user_group = MenuHelper.get_id()
        if (new_id == "") or (user_group == ""):
            return False

        menu_helper = MenuHelper()
        first_name = menu_helper.get_name("first")
        last_name = menu_helper.get_name("last")
        username = menu_helper.get_check_user_input("username", user_group)
        password = menu_helper.register_new_password()
        birthday = menu_helper.get_birthday()
        telephone = menu_helper.valid_local_phone()
        address = menu_helper.get_address()
        postcode = menu_helper.valid_postcode()

        insert_query = SQLQuery("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        insert_query.executeCommit((new_id, username, password, birthday, first_name, last_name,
                                    telephone, address, postcode, user_group, "T"))

        Parser.print_clean("Successfully Registered But Currently Deactivated.\n")
        return True

    def get_check_user_input(self, parameter_name, user_group):
        """
        :param str parameter_name: The name of the parameter for Admin to enter
        :param str user_group: Patient or GP
        :return: New unique Username that is not currently being used
        """
        while True:
            try:
                parameter = Parser.string_parser("Please enter {0} of {1}: ".format(parameter_name, user_group))
                # check if it exists in table, if it does ask again
                exists_query = SQLQuery("SELECT 1 FROM Users WHERE {0} = '{1}'".format(parameter_name, parameter))\
                    .executeFetchAll()
                if exists_query:
                    raise InValidUsernameError
                else:
                    return parameter
            except InValidUsernameError:
                print("{0} already exists. Please choose another.\n".format(parameter_name))
                input("Press Enter to continue...")

    def register_new_password(self):
        """
        :return: Check for valid new password
        """
        while True:
            Parser.print_clean("Any leading or trailing empty spaces will be removed.")
            try:
                password = getpass("Enter new password: ").strip()
                password_confirm = getpass("Enter new password again: ").strip()
                if (password != password_confirm) and (password != ""):
                    raise InValidPasswordError
                else:
                    return PasswordHelper.hashPW(password)
            except InValidPasswordError:
                print("Passwords do not match. Please try again.\n")
                input("Press Enter to continue...")

    @staticmethod
    def get_id():
        """
        :return: Valid user ID and type of user
        """
        while True:
            user_group = Parser.selection_parser(options={"A": "GP", "B": "Patient", "--back": "back"})
            Parser.print_clean()
            if user_group == "--back":
                return "", ""
            else:
                if user_group == "A":
                    new_id = Parser.gp_no_parser()
                    user_group = "GP"
                else:
                    new_id = Parser.nhs_no_parser()
                    user_group = "Patient"
                return new_id, user_group

    @staticmethod
    def valid_local_phone():
        """
        :return: return a valid UK phone number
        """
        while True:
            try:
                phone_number = Parser.string_parser("Please enter local UK phone number: ").strip()
                if (len(phone_number) == 11) and \
                        (not any([char in phone_number for char in ["+", "-", "(", ")"]])) and \
                        (not phone_number.isupper()) and (not phone_number.islower()):
                    return EncryptionHelper().encryptToBits(phone_number)
                else:
                    raise InValidPhoneNumberError
            except InValidPhoneNumberError:
                print("Invalid Phone Number. Please try again.\n")
                input("Press Enter to continue...")

    @staticmethod
    def valid_postcode():
        """
        :return: return a valid UK postcode
        """
        while True:
            try:
                temp_postcode = Parser.string_parser("Please enter primary home postcode: ").strip().replace(" ", "")
                if (len(temp_postcode) != 5) and (len(temp_postcode) != 7):
                    raise InValidPostcodeError
                else:
                    return EncryptionHelper().encryptToBits(temp_postcode)
            except InValidPostcodeError:
                print("Invalid Postcode. Please try again.\n")
                input("Press Enter to continue...")

    @staticmethod
    def get_address():
        """
        :return: Encrypted First line of GP or Patient UK address
        """
        return EncryptionHelper().encryptToBits(Parser.string_parser("Please enter primary home address (one line): "))

    @staticmethod
    def get_name(name_type):
        """
        :param str name_type: First/Last Name flag for user input
        :return: Encrypted new first/last name of user
        """
        return EncryptionHelper().encryptToBits(Parser.string_parser(
            "Please enter {0} name: ".format(name_type)))

    @staticmethod
    def get_birthday():
        """
        :return: Encrypted User birthday
        """
        return EncryptionHelper().encryptToBits(str(Parser.date_parser("Please enter birthday: ",
                                                                       allow_back=False, allow_past=True)))

    @staticmethod
    def dispatcher(username, user_type):
        """
        :param str username: Username of account
        :param str user_type: Type of account
        :return: Main menu of Logged in user
        """
        if user_type == "Admin":
            from admin import Admin
            user = Admin(username)
        elif user_type == "GP":
            from gp import GP
            user = GP(username)
        else:
            from patient import Patient
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
        """
        Personalised logged in message to user.
        """
        Parser.print_clean(f"Login Successful. Hello {self.first_name}")
        return True

    def print_information(self):
        """
        Display all User information.
        """
        Parser.print_clean(tabulate([("User Type:", self.user_type),
                                     ("First Name: ", self.first_name),
                                     ("Last Name: ", self.last_name),
                                     ("Birthday: ", self.birthday),
                                     ("Phone No: ", self.phone_no),
                                     ("Home Address: ", self.home_address),
                                     ("Post Code: ", self.postcode)
                                     ]))
        return True


if __name__ == '__main__':
    """Main Program starts here."""

    # Exception handling if database not present/cannot connect
    # Exception handling of sqlite3.DatabaseError: database disk image is malformed
    try:
        from urllib.request import pathname2url
        database = 'file:{}?mode=rw'.format(pathname2url("GPDB.db"))
        conn = sqlite3.connect(database, uri=True)
    except sqlite3.OperationalError:
        Parser.print_clean("Database does not exist.")
        Parser.user_quit()
    except sqlite3.DatabaseError:
        Parser.print_clean("Database disk image is malformed.")
        Parser.user_quit()

    while True:
        print("Welcome to Group 6 GP System")
        option_selection = Parser.selection_parser(options={"R": "register", "L": "login", "--quit": "quit"})

        if option_selection == 'L':
            current_user = MenuHelper.login()
            MenuHelper.dispatcher(current_user["username"], current_user["user_type"])
        else:
            result = MenuHelper.register()
            if result:
                Parser.print_clean("Contact an Administrator to activate account.\n")
                Parser.user_quit()

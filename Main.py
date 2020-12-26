from ParserHelp import Parser
from DatabaseHelp import SQLQuery
from Encryption import EncryptionHelper
from Encryption import PasswordHelper
from getpass import getpass
from tabulate import tabulate
from Exceptions import DBRecordError


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
    def register():
        """
        Register a new GP or Patient Account.
        """
        new_id, user_group = MenuHelper.getId()
        if (new_id == "") or (user_group == ""):
            return

        username = MenuHelper.getCheckUserInput("username", user_group)
        password = MenuHelper.registerNewPassword()
        birthday = MenuHelper.getBirthday()
        Parser.print_clean("\n")

        first_name = MenuHelper.getName("first")
        Parser.print_clean("\n")

        last_name = MenuHelper.getName("last")
        Parser.print_clean("\n")

        telephone = MenuHelper.validLocalPhoneNumber()
        address = MenuHelper.getAddress()
        Parser.print_clean("\n")

        postcode = MenuHelper.validPostcode()

        insert_query = SQLQuery("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        insert_query.executeCommit((new_id, username, password, birthday, first_name, last_name,
                                    telephone, address, postcode, user_group, "T"))

        Parser.print_clean("Successfully Registered. Contact an Admin to activate account.\n")
        Parser.user_quit()

    @staticmethod
    def getAddress():
        """
        :return: Encrypted First line of GP or Patient UK address
        """
        return EncryptionHelper().encryptToBits(Parser.string_parser("Please enter primary home address (one line): "))

    @staticmethod
    def getName(name_type):
        """
        :param str name_type: First/Last Name flag for user input
        :return: Encrypted new first/last name of user
        """
        return EncryptionHelper().encryptToBits(Parser.string_parser(
            "Please enter {0} name: ".format(name_type)))

    @staticmethod
    def getBirthday():
        """
        :return: Encrypted User birthday
        """
        return EncryptionHelper().encryptToBits(str(Parser.date_parser("Please enter birthday: ",
                                                                       allow_back=False, allow_past=True)))

    @staticmethod
    def getId():
        """
        :return: Valid user ID and type of user
        """
        while True:
            Parser.print_clean("\nPress --back to go back.")
            user_group = Parser.selection_parser(options={"A": "GP", "B": "Patient", "--back": "back"})
            if user_group == "--back":
                Parser.print_clean("\n")
                return "", ""
            elif user_group == "A":
                new_id = Parser.gp_no_parser()
                user_group = "GP"
                Parser.print_clean("\n")
                return new_id, user_group
            else:
                new_id = Parser.nhs_no_parser()
                user_group = "Patient"
                Parser.print_clean("\n")
                return new_id, user_group

    @staticmethod
    def getCheckUserInput(parameter_name, user_group):
        """
        :param str parameter_name: The name of the parameter for Admin to enter
        :param str user_group: Patient or GP
        :return: New unique Username that is not currently being used
        """
        while True:
            parameter = Parser.string_parser("Please enter {0} of {1}: ".format(parameter_name, user_group))
            # check if it exists in table, if it does ask again
            exists_query = SQLQuery("SELECT 1 FROM Users WHERE {0} = '{1}'".format(parameter_name, parameter))\
                .executeFetchAll()
            if exists_query:
                Parser.print_clean("{0} already exists. Please choose another.\n".format(parameter_name))
                continue
            else:
                Parser.print_clean("{0} approved.\n".format(parameter_name[0].upper() + parameter_name[1:]))
                return parameter

    @staticmethod
    def registerNewPassword():
        """
        :return: Check for valid new password
        """
        while True:
            Parser.print_clean("Any leading or trailing empty spaces will be removed.")
            password = getpass("Enter new password: ").strip()
            password_confirm = getpass("Enter new password again: ").strip()
            if (password != password_confirm) and (password != ""):
                Parser.print_clean("Passwords do not match. Please try again.\n")
            else:
                Parser.print_clean("Passwords Match.\n")
                return PasswordHelper.hashPW(password)

    @staticmethod
    def validLocalPhoneNumber():
        """
        :return: return a valid UK phone number
        """
        while True:
            phone_number = Parser.string_parser("Please enter local UK phone number: ").strip()
            if (len(phone_number) == 11) and \
                    (not any([char in phone_number for char in ["+", "-", "(", ")"]])) and \
                    (not phone_number.isupper()) and (not phone_number.islower()):
                Parser.print_clean("Valid Phone Number.\n")
                return EncryptionHelper().encryptToBits(phone_number)
            else:
                Parser.print_clean("Invalid Phone Number. Please try again.\n")

    @staticmethod
    def validPostcode():
        """
        :return: return a valid UK postcode
        """
        while True:
            temp_postcode = Parser.string_parser("Please enter primary home postcode: ").strip().replace(" ", "")
            if (len(temp_postcode) != 5) and (len(temp_postcode) != 7):
                Parser.print_clean("Invalid Postcode. Please try again.\n")
            else:
                Parser.print_clean("Valid Postcode.\n")
                return EncryptionHelper().encryptToBits(temp_postcode)

    @staticmethod
    def dispatcher(username, user_type):
        """
        :param str username: Username of account
        :param str user_type: Type of account
        :return: Main menu of Logged in user
        """
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
        """
        Personalised logged in message to user.
        """
        Parser.print_clean(f"Login Successful. Hello {self.first_name}")
        return True

    def print_information(self):
        """
        Display all User information.
        """
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
    """Main Program starts here."""

    # Exception handling if database not present/cannot connect
    # conn = create_connection("GPDB.db")

    while True:
        print("Welcome to Group 6 GP System")
        option_selection = Parser.selection_parser(options={"R": "register", "L": "login", "--quit": "quit"})

        if option_selection == 'L':
            current_user = MenuHelper.login()
            MenuHelper.dispatcher(current_user["username"], current_user["user_type"])
        else:
            MenuHelper.register()

import getpass
from tabulate import tabulate
from encryption import EncryptionHelper, PasswordHelper
from parser_help import Parser
from database_help import SQLQuery
from main import User, MenuHelper


class AdminNavigator(User):
    """Navigate through Admin features and functionality once logged in."""

    def main_menu(self):
        """
        Main Menu for Admin-type users.
        """
        while True:
            user_input = Parser.selection_parser(
                options={"A": "View Records", "B": "Add New GP or Patient", "C": "Edit GP or Patient",
                         "D": "Delete Existing GP or Patient", "--logout": "logout"})
            if user_input == "--logout":
                Parser.user_quit()
            elif user_input == "A":
                self.viewRecords()
            elif user_input == "B":
                self.addGPPatient()
            elif user_input == "C":
                self.editGPPatient()
            else:
                self.deleteGPPatient()

    @staticmethod
    def viewRecords():
        """
        User interface for viewing the desired records
        """
        while True:
            record_viewer = Parser.selection_parser(
                options={"A": "View Patients", "B": "View GPs",
                         "C": "View Available Timeslots", "D": "View Patient Appointments",
                         "E": "View Patient Prescriptions", "--back": "back"})

            if record_viewer == "--back":
                return
            elif record_viewer == "C":
                query_string = "SELECT * FROM available_time"
                headers = ("StaffID", "Timeslot")
            elif record_viewer == "D":
                query_string = "SELECT * FROM Visit"
                headers = ("BookingNo", "NHSNo", "StaffID", "Timeslot", "Confirmed", "Attended", "Diagnosis", "Notes")
            elif record_viewer == "E":
                query_string = "SELECT * FROM prescription"
                headers = ("BookingNo", "DrugName", "Quantity", "Instructions")
            else:
                query_string = "SELECT ID, Username, Deactivated, birthday, firstName, lastName, phoneNo, " \
                               "HomeAddress, postCode FROM USERS WHERE UserType = '{0}'"
                headers = ("ID", "Username", "Deactivated", "Birthday", "First Name", "Last Name", "PhoneNo", "Address",
                           "Postcode")
                if record_viewer == "A":
                    query_string = query_string.format("Patient")
                else:
                    query_string = query_string.format("GP")

            query = SQLQuery(query_string)
            all_data = query.executeFetchAll(decrypter=EncryptionHelper())

            if len(list(all_data)) == 0:
                Parser.print_clean("No records Available.\n")
                continue

            Parser.print_clean(tabulate(all_data, headers))
            Parser.print_clean("Completed operation.\n")
            continue

    def addGPPatient(self):
        """
        Updated table with new GP or patient record
        """
        new_id, user_group = self.getId()
        if (new_id == "") or (user_group == ""):
            return

        username = self.getCheckUserInput("username", user_group)
        password = self.registerNewPassword()
        birthday = self.getBirthday()
        first_name = self.getName("first")
        last_name = self.getName("last")
        telephone = self.validLocalPhoneNumber()
        address = self.getAddress()
        postcode = self.validPostcode()

        insert_query = SQLQuery("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        insert_query.executeCommit((new_id, username, password, birthday, first_name, last_name,
                                    telephone, address, postcode, user_group, "F"))
        Parser.print_clean("Successfully Added to Database. Going back to home page.\n")

    def editGPPatient(self):
        """
        Edit existing GP or Patient Record
        """
        # show all GPs and Patients
        view_all_gps_and_patients = SQLQuery("SELECT username FROM Users WHERE UserType = 'GP' or "
                                             "UserType = 'Patient'")
        view_all_gps_and_patients_result = list(view_all_gps_and_patients.executeFetchAll())

        if len(view_all_gps_and_patients_result) == 0:
            Parser.print_clean("No Patients or GPs registered. Please add before coming back.\n")
            return

        all_gps_and_patients_table, gps_and_patients = self.viewAllPatientsAndGPs(view_all_gps_and_patients_result)
        Parser.print_clean(tabulate(all_gps_and_patients_table, headers=("ID", "Username")))

        # select a user from the table
        while True:
            Parser.print_clean("Press --back to go back.")
            selected_user = Parser.string_parser("Enter the username to edit the profile: ")
            if selected_user == "--back":
                Parser.print_clean()
                break
            if selected_user not in gps_and_patients:
                Parser.print_clean("This username does not exist. Please enter a valid username.\n")
                continue
            else:
                Parser.print_clean()
                record_editor = Parser.selection_parser(
                    options={"A": "Update Password", "B": "Update Birthday",
                             "C": "Update First Name", "D": "Update Last Name",
                             "E": "Update Phone Number", "F": "Update Home Address",
                             "G": "Update Postcode", "H": "Switch Activation Status",
                             "--back": "back"})

                if record_editor == "--back":
                    Parser.print_clean()
                    return
                elif record_editor == "A":
                    new_parameter_value = self.registerNewPassword()
                    parameter = "passCode"
                elif record_editor == "B":
                    new_parameter_value = self.getBirthday()
                    parameter = "birthday"
                elif record_editor == "C":
                    new_parameter_value = self.getName("first")
                    parameter = "firstName"
                elif record_editor == "D":
                    new_parameter_value = self.getName("last")
                    parameter = "lastName"
                elif record_editor == "E":
                    new_parameter_value = self.validLocalPhoneNumber()
                    parameter = "phoneNo"
                elif record_editor == "F":
                    new_parameter_value = self.getAddress()
                    parameter = "HomeAddress"
                elif record_editor == "G":
                    new_parameter_value = self.validPostcode()
                    parameter = "postCode"
                else:
                    current_status = SQLQuery("SELECT Deactivated FROM Users WHERE username = '{0}'"
                                              .format(selected_user)).executeFetchAll()
                    parameter = "Deactivated"
                    if current_status[0][0] == "F":
                        new_parameter_value, status = "T", parameter
                    else:
                        new_parameter_value, status = "F", parameter[2].upper() + parameter[3:]

                    Parser.print_clean("User {0} will be {1}.".format(selected_user, status))

                self.updateParameterRecord(selected_user, parameter, new_parameter_value)
                Parser.print_clean("Successfully Updated to Database. Going back to home page.\n")
                return

    def deleteGPPatient(self):
        """
        updated table with the deleted GP record
        """
        # show all users that are deactivated for deletion
        all_deactivated_gps = SQLQuery("SELECT username FROM Users WHERE Deactivated = 'T' AND "
                                       "((UserType = 'GP') OR (UserType = 'Patient'))")
        all_deactivated_gps_result = list(all_deactivated_gps.executeFetchAll())

        if len(all_deactivated_gps_result) == 0:
            Parser.print_clean("No deactivated GPs available to delete.\n")
            return

        all_deactivated_gps_table, gps_and_patients = self.viewAllPatientsAndGPs(all_deactivated_gps_result)
        Parser.print_clean(tabulate(all_deactivated_gps_table, headers=("ID", "Username")))

        # select a deactivated GP account to delete
        while True:
            Parser.print_clean("\nPress --back to go back.")
            selected_gp = Parser.string_parser("Write the name of GP to delete: ")
            if selected_gp == "--back":
                Parser.print_clean()
                break
            if selected_gp not in gps_and_patients:
                Parser.print_clean("\nThis name does not exist. Please try again.")
                continue
            else:
                # delete query, make sure to delete all presence of that user
                delete_query = SQLQuery("DELETE FROM Users WHERE username=:who")
                delete_query.executeCommit({"who": selected_gp})
                Parser.print_clean("GP {0} deleted from Users table.\n".format(selected_gp))
                return

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
                        "Please enter new {0} name: ".format(name_type)))

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
            Parser.print_clean("Press --back to go back.")
            user_group = Parser.string_parser("Please enter type of user (GP or Patient): ").lower().strip()
            if user_group == "--back":
                Parser.print_clean()
                return "", ""
            if user_group == "gp":
                new_id = Parser.gp_no_parser()
                user_group = user_group.upper()
                return new_id, user_group
            elif user_group == "patient":
                new_id = Parser.nhs_no_parser()
                user_group = user_group[0].upper() + user_group[1:]
                return new_id, user_group
            else:
                print("Incorrect input. Please Try again.\n")
                continue

    @staticmethod
    def viewAllPatientsAndGPs(all_results):
        """
        :param list all_results: All results from query
        :return: List of all GPs and Patients with ID and another list with only names of patient/GP
        """
        all_gps_and_patients_table, gp_and_patient = [], []
        for nameIndex in range(len(all_results)):
            gp_and_patient.append(all_results[nameIndex][0])
            all_gps_and_patients_table.append([nameIndex + 1, all_results[nameIndex][0]])
        return all_gps_and_patients_table, gp_and_patient

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
            exists_query = SQLQuery("SELECT 1 FROM Users WHERE {0} =:who".format(parameter_name))\
                .executeCommit({"who": parameter})
            if exists_query > 0:
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
            Parser.print_clean("Any empty spaces on either ends will be removed.")
            password = getpass.getpass("Enter new password: ").strip()
            password_confirm = getpass.getpass("Enter new password again: ").strip()
            if (password != password_confirm) and (password != ""):
                Parser.print_clean("Passwords do not match. Please try again.\n")
            else:
                Parser.print_clean("Passwords Match.")
                return PasswordHelper.hashPW(password)

    @staticmethod
    def validLocalPhoneNumber():
        """
        :return: return a valid UK phone number
        """
        while True:
            phone_number = Parser.string_parser("Please enter local UK phone number: ")
            if (len(phone_number.strip()) == 11) and \
                    (not any([char in phone_number for char in ["+", "-", "(", ")"]])):
                Parser.print_clean("Valid Phone Number.\n")
                return EncryptionHelper().encryptToBits(phone_number)
            else:
                Parser.print_clean("Invalid Phone Number. Please try again.")

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
    def updateParameterRecord(selected_user, parameter, new_parameter_value):
        """
        :param selected_user: Current user, admin is changing
        :param parameter: Current table column admin is changing
        :param new_parameter_value: New value to change within the table column of the currently selected user
        :return: Updated Users table
        """
        SQLQuery("UPDATE Users SET {0} = ? WHERE username = ?".format(parameter)).executeCommit((new_parameter_value,
                                                                                                 selected_user))


if __name__ == "__main__":
    # loginParam = loginHelp.Login()
    # user = currentUser(loginParam[0], loginParam[1])
    # current_admin = AdminNavigator()
    # AdminNavigator().mainNavigator("testAdmin124")

    # Q = SQLQuery("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    # EH = EncryptionHelper()
    # # noinspection PyTypeChecker
    # result = Q.executeCommit(("AD1",
    #                           "testAdmin124",
    #                           PasswordHelper.hashPW("testAdmin"),
    #                           EH.encryptToBits("1991-01-04"),
    #                           EH.encryptToBits("testAdminFirstName"),
    #                           EH.encryptToBits("testAdminLastName"),
    #                           EH.encryptToBits("0123450233"),
    #                           EH.encryptToBits("testAdminHome Address, test Road"),
    #                           EH.encryptToBits("A1 7RT"),
    #                           "Admin",
    #                           "F"))

    current_user = MenuHelper.login()
    MenuHelper.dispatcher(current_user["username"], current_user["user_type"])
    AdminNavigator(current_user).main_menu()

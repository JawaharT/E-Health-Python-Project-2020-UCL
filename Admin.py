import os
from tabulate import tabulate

import getpass
from encryption import encryptionHelper, passwordHelper
from login import currentUser, loginHelp
from parserHelp import parser
from databaseHelp import SQLQuerry
import time
import sys


class AdminNavigator:
    """Navigate through Admin features and functionality once logged in as one."""

    def mainNavigator(self, admin_user):
        """
        :return: divert user into the main admin functionalities
        """
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print(f"Login Successful. Hello {admin_user.firstName}")
        user_info_table = [("User Type:", admin_user.UserType),
                           ("First Name: ", admin_user.firstName),
                           ("Last Name: ", admin_user.lastName),
                           ("Birthday: ", admin_user.birthday),
                           ("Phone No: ", admin_user.phoneNo),
                           ("Home Address: ", admin_user.HomeAddress),
                           ("Post Code: ", admin_user.postCode)]
        print(tabulate(user_info_table))

        while True:
            user_input = parser.selectionParser(
                options={"A": "View Records", "B": "Add New GP or Patient", "C": "Edit GP or Patient",
                         "D": "Delete Existing GP or Patient", "--logout": "logout"})
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
                # AdminNavigator().viewRecords()
                self.viewRecords()
            elif current_page == "B":
                self.addGPPatient()
            elif current_page == "C":
                self.editGPPatient()
            else:
                self.deleteGPPatient()

    @staticmethod
    def viewRecords():
        """
        :return: User interface for viewing the desired records
        """
        while True:
            record_viewer = parser.selectionParser(
                options={"A": "View Patients", "B": "View GPs",
                         "C": "View Available Timeslots", "D": "View Patient Appointments",
                         "E": "View Patient Prescriptions", "--back": "back"})

            if record_viewer == "--back":
                return
            elif record_viewer == "A":
                query = SQLQuerry("SELECT ID, Username, Deactivated, birthday, firstName, lastName, phoneNo,"
                                  " HomeAddress, postCode FROM USERS WHERE UserType = 'Patient'")
                headers = ("ID", "Username", "Deactivated", "Birthday", "First Name", "Last Name", "PhoneNo", "Address",
                           "Postcode")
                start_of_decryption, decrypt = 3, True
            elif record_viewer == "B":
                query = SQLQuerry("SELECT ID, Username, Deactivated, birthday, firstName, lastName, phoneNo,"
                                  " HomeAddress, postCode FROM USERS WHERE UserType = 'GP'")
                headers = ("ID", "Username", "Deactivated", "Birthday", "First Name", "Last Name", "PhoneNo", "Address",
                           "Postcode")
                start_of_decryption, decrypt = 3, True
            elif record_viewer == "C":
                query = SQLQuerry("SELECT * FROM available_time")
                headers = ("StaffID", "Timeslot")
                start_of_decryption, decrypt = len(headers), False
            elif record_viewer == "D":
                query = SQLQuerry("SELECT * FROM Visit")
                headers = ("BookingNo", "NHSNo", "StaffID", "Timeslot", "Confirmed", "Attended", "Diagnosis", "Notes")
                start_of_decryption, decrypt = len(headers), False
            elif record_viewer == "E":
                query = SQLQuerry("SELECT * FROM prescription")
                headers = ("BookingNo", "DrugName", "Quantity", "Instructions")
                start_of_decryption, decrypt = len(headers), False
            else:
                print("Not a valid selection.\n")
                continue

            all_data = query.executeFetchAll()
            encryption_helper = encryptionHelper()

            if len(all_data) == 0:
                print("No records Available.\n")
                continue

            decrypted_data = []
            for recordNumber in range(len(all_data)):
                current_record = []
                if start_of_decryption != 0:
                    for not_encrypted_column_number in range(0, start_of_decryption):
                        current_record.append(all_data[recordNumber][not_encrypted_column_number])
                # decrypting the encrypted data
                if decrypt:
                    for columnNumber in range(start_of_decryption, len(headers)):
                        current_record.append(encryption_helper.decryptMessage(all_data[recordNumber][columnNumber]))
                decrypted_data.append(current_record)

            print(tabulate(decrypted_data, headers))
            print("Completed operation.\n")
            continue

    def addGPPatient(self):
        """
        :return: updated table with new GP or patient record
        """
        new_id, user_group = AdminNavigator().get_id()
        if (new_id == "") or (user_group == ""):
            return

        username = self.getCheckUserInput("username", user_group)
        password = self.registerNewPassword()

        encryption_helper = encryptionHelper()
        birthday = encryption_helper.encryptToBits(str(parser().dateParser("Please enter birthday: ", False).date()))
        first_name = encryption_helper.encryptToBits(input("Please enter first name: "))
        last_name = encryption_helper.encryptToBits(input("Please enter last name: "))

        # check for only local phone numbers and 11 digits only
        telephone = self.validLocalPhoneNumber(encryption_helper)
        address = encryption_helper.encryptToBits(input("Please enter primary home address (one line): "))

        # check for only 5 or 7 chars
        postcode = self.validPostcode(encryption_helper)

        insert_query = SQLQuerry("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        insert_query.executeCommit((new_id, username, password, birthday, first_name, last_name,
                                    telephone, address, postcode, user_group, "F"))
        print("Successfully Added to Database. Going back to home page.\n")
        return

    def editGPPatient(self):
        """
        :return: Edit existing GP or Patient Record
        """
        # show all GPs and Patients
        view_all_gps_and_patients = SQLQuerry("SELECT username FROM Users WHERE UserType = 'GP' or "
                                              "UserType = 'Patient'")
        view_all_gps_and_patients_result = view_all_gps_and_patients.executeFetchAll()

        if len(view_all_gps_and_patients_result) == 0:
            print("No Patients or GPs registered. Please add before coming back.\n")
            return

        all_gps_and_patients_table, gps_and_patients = self.viewAllPatientsAndGPs(view_all_gps_and_patients_result)
        print(tabulate(all_gps_and_patients_table, headers=("ID", "Username")))

        # select a user from the table
        while True:
            print("Press --back to go back.")
            selected_user = input("Enter the username to edit the profile: ")
            if selected_user == "--back":
                print()
                break
            if selected_user not in gps_and_patients:
                print("This username does not exist. Please enter a valid username.\n")
                continue
            else:
                print()
                record_editor = parser.selectionParser(
                    options={"A": "Update Password", "B": "Update Birthday",
                             "C": "Update First Name", "D": "Update Last Name",
                             "E": "Update Phone Number", "F": "Update Home Address",
                             "G": "Update Postcode", "H": "Switch Activation Status",
                             "--back": "back"})

                encryption_helper = encryptionHelper()
                if record_editor == "--back":
                    print()
                    return
                elif record_editor == "A":
                    new_parameter_value = self.registerNewPassword()
                    parameter = "passCode"
                elif record_editor == "B":
                    new_parameter_value = encryption_helper.encryptToBits(
                        str(parser().dateParser("Please enter birthday: ", False).date()))
                    parameter = "birthday"
                elif record_editor == "C":
                    new_parameter_value = encryption_helper.encryptToBits(input("Please enter new first name: "))
                    parameter = "firstName"
                elif record_editor == "D":
                    new_parameter_value = encryption_helper.encryptToBits(input("Please enter new last name: "))
                    parameter = "lastName"
                elif record_editor == "E":
                    new_parameter_value = self.validLocalPhoneNumber(encryption_helper)
                    parameter = "phoneNo"
                elif record_editor == "F":
                    new_parameter_value = encryption_helper.encryptToBits(
                        input("Please enter primary home address (one line): "))
                    parameter = "HomeAddress"
                elif record_editor == "G":
                    new_parameter_value = self.validPostcode(encryption_helper)
                    parameter = "postCode"
                else:
                    current_status = SQLQuerry("SELECT Deactivated FROM Users WHERE username = '{0}'".
                                               format(selected_user)).executeFetchAll()[0][0]
                    parameter = "Deactivated"
                    if current_status == "F":
                        new_parameter_value, status = "T", parameter
                    else:
                        new_parameter_value, status = "F", parameter[2].upper() + parameter[3:]

                    print("User {0} will be {1}.".format(selected_user, status))

                self.updateParameterRecord(selected_user, parameter, new_parameter_value)
                print("Successfully Updated to Database. Going back to home page.\n")
                return

    def deleteGPPatient(self):
        """
        :return: updated table with the deleted GP record
        """
        # show all users that are deactivated for deletion
        all_deactivated_gps = SQLQuerry("SELECT username FROM Users WHERE Deactivated = 'T' AND "
                                        "((UserType = 'GP') OR (UserType = 'Patient'))")
        all_deactivated_gps_result = all_deactivated_gps.executeFetchAll()

        if len(all_deactivated_gps_result) == 0:
            print("No deactivated GPs available to delete.\n")
            return

        all_deactivated_gps_table, gps_and_patients = self.viewAllPatientsAndGPs(all_deactivated_gps_result)
        print(tabulate(all_deactivated_gps_table, headers=("ID", "Username")))

        # select a deactivated GP account to delete
        while True:
            print("\nPress --back to go back.")
            selected_gp = input("Write the name of GP to delete: ")
            if selected_gp == "--back":
                print()
                break
            if selected_gp not in gps_and_patients:
                print("\nThis name does not exist. Please try again.")
                continue
            else:
                # delete query, make sure to delete all presence of that user
                delete_query = SQLQuerry("DELETE FROM Users WHERE username=:who")
                delete_query.executeCommit({"who": selected_gp})
                print("GP {0} deleted from Users table.\n".format(selected_gp))
                return

    @staticmethod
    def get_id():
        while True:
            print("Press --back to go back.")
            user_group = input("Please enter type of user (GP or Patient): ").lower().strip()
            if user_group == "--back":
                print()
                return "", ""
            if user_group == "gp":
                new_id = parser().GPStaffNoParser()
                user_group = user_group.upper()
                return new_id, user_group
            elif user_group == "patient":
                new_id = parser().nhsNoParser()
                user_group = user_group[0].upper() + user_group[1:]
                return new_id, user_group
            else:
                print("Incorrect input. Please Try again.\n")
                continue

    @staticmethod
    def viewAllPatientsAndGPs(all_results):
        all_gps_and_patients_table, gp_and_patient = [], []
        for nameIndex in range(len(all_results)):
            gp_and_patient.append(all_results[nameIndex][0])
            all_gps_and_patients_table.append([nameIndex + 1, all_results[nameIndex][0]])
        return all_gps_and_patients_table, gp_and_patient

    @staticmethod
    def getCheckUserInput(parameter_name, user_group):
        """
        :param parameter_name: The name of the parameter for Admin to enter
        :param user_group: Patient or GP
        :return: New unique Username that is not currently being used
        """
        while True:
            parameter = input("Please enter {0} of {1}: ".format(parameter_name, user_group))
            # check if it exists in table, if it does ask again
            exists_query = SQLQuerry("SELECT 1 FROM Users WHERE {0} =:who".format(parameter_name)) \
                .executeCommit({"who": parameter})
            # print(existsQuery)
            if exists_query > 0:
                print("{0} already exists. Please choose another.\n".format(parameter_name))
                continue
            else:
                print("{0} approved.\n".format(parameter_name))
                return parameter

    @staticmethod
    def registerNewPassword():
        """
        :return: check for valid new password that will match
        """
        while True:
            password = getpass.getpass("Enter new password: ")
            password_confirm = getpass.getpass("Enter new password again: ")
            if password != password_confirm:
                print("Passwords do not match. Please try again.\n")
            else:
                print("Passwords Match.\n")
                return passwordHelper.hashPW(password)

    @staticmethod
    def validLocalPhoneNumber(encryption_helper):
        """
        :return: return a valid UK phone number
        """
        while True:
            phone_number = input("Please enter local UK phone number: ")
            if (len(phone_number.strip()) == 11) and \
                    (not any([char in phone_number for char in ["+", "-", "(", ")"]])):
                print("Valid Phone Number.\n")
                return encryption_helper.encryptToBits(phone_number)
            else:
                print("Invalid Phone Number. Please try again.\n")

    @staticmethod
    def validPostcode(encryption_helper):
        """
        :return: return a valid UK postcode
        """
        while True:
            temp_postcode = input("Please enter primary home postcode: ").strip().replace(" ", "")
            if (len(temp_postcode) != 5) and (len(temp_postcode) != 7):
                print("Invalid Postcode. Please try again.\n")
            else:
                print("Valid Postcode.\n")
                return encryption_helper.encryptToBits(temp_postcode)

    @staticmethod
    def updateParameterRecord(selected_user, parameter, new_parameter_value):
        """
        :param selected_user: Current user, admin is changing
        :param parameter: Current table column admin is changing
        :param new_parameter_value: New value to change within the table column of the currently selected user
        :return: Updated Users table
        """
        SQLQuerry("UPDATE Users SET {0} = ? WHERE username = ?".format(parameter))\
            .executeCommit((new_parameter_value, selected_user))


if __name__ == "__main__":
    loginParam = loginHelp.Login()
    user = currentUser(loginParam[0], loginParam[1])
    current_admin = AdminNavigator()
    current_admin.mainNavigator(user)

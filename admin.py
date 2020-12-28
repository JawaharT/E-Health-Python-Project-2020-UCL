from tabulate import tabulate
from encryption import EncryptionHelper
from parser_help import Parser
from database_help import SQLQuery
from main import User, MenuHelper


class Admin(User):
    """Navigate through Admin features and functionality once logged in."""

    def main_menu(self):
        """
        Main Menu for Admin-type users.
        """
        while True:
            print("You're currently viewing main menu options for Admin {}.".format(self.username))
            user_input = Parser.selection_parser(
                options={"A": "View Records", "B": "Add New GP or Patient", "C": "Edit GP or Patient",
                         "D": "Delete Existing GP or Patient", "--logout": "logout"})
            if user_input == "--logout":
                Parser.user_quit()
            elif user_input == "A":
                self.view_records()
            elif user_input == "B":
                self.add_gp_patient()
            elif user_input == "C":
                self.edit_gp_patient()
            else:
                self.delete_gp_patient()

    def view_records(self):
        """
        User interface for viewing the desired records
        """
        while True:
            record_viewer = Parser.selection_parser(
                options={"A": "View Patients", "B": "View GPs",
                         "C": "View Available Timeslots", "D": "View Patient Appointments",
                         "E": "View Patient Prescriptions", "--back": "back"})

            parameters = ()
            if record_viewer == "--back":
                Parser.print_clean()
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
                               "HomeAddress, postCode FROM USERS WHERE UserType == ?"
                headers = ("ID", "Username", "Deactivated", "Birthday", "First Name", "Last Name", "PhoneNo", "Address",
                           "Postcode")
                if record_viewer == "A":
                    user_type = "Patient"
                else:
                    user_type = "GP"
                parameters = (user_type,)

            query = SQLQuery(query_string)
            all_data = query.executeFetchAll(decrypter=EncryptionHelper(), parameters=parameters)

            if len(list(all_data)) == 0:
                Parser.print_clean("No records Available.\n")
                continue

            for row in all_data:
                current = []
                for index, title in enumerate(headers):
                    current.append((title+":", row[index]))
                print(tabulate(current))

            print("Completed operation.\n")
            continue

    def add_gp_patient(self):
        """
        Updated table with new GP or patient record
        """
        Parser.print_clean()
        MenuHelper().register()

    def edit_gp_patient(self):
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

        # select a user from the table
        while True:
            all_gps_and_patients_table, gps_and_patients = self.view_all_patients_and_GPs(
                view_all_gps_and_patients_result)
            selected_user_number = Parser.selection_parser(options=all_gps_and_patients_table)
            selected_user = all_gps_and_patients_table[selected_user_number]
            if selected_user == "back":
                Parser.print_clean()
                break
            else:
                record_editor = Parser.selection_parser(
                    options={"A": "Update Password", "B": "Update Birthday",
                             "C": "Update First Name", "D": "Update Last Name",
                             "E": "Update Phone Number", "F": "Update Home Address",
                             "G": "Update Postcode", "H": "Switch Activation Status",
                             "--back": "back"})

                menu = MenuHelper()
                if record_editor == "--back":
                    Parser.print_clean()
                    return
                elif record_editor == "":
                    new_parameter_value = menu.register_new_password()
                    parameter = "passCode"
                elif record_editor == "B":
                    new_parameter_value = menu.get_birthday()
                    parameter = "birthday"
                elif record_editor == "C":
                    new_parameter_value = menu.get_name("first")
                    parameter = "firstName"
                elif record_editor == "D":
                    new_parameter_value = menu.get_name("last")
                    parameter = "lastName"
                elif record_editor == "E":
                    new_parameter_value = menu.valid_local_phone()
                    parameter = "phoneNo"
                elif record_editor == "F":
                    new_parameter_value = menu.get_address()
                    parameter = "HomeAddress"
                elif record_editor == "G":
                    new_parameter_value = menu.valid_postcode()
                    parameter = "postCode"
                else:
                    current_status = SQLQuery("SELECT Deactivated FROM Users WHERE username = '{0}'"
                                              .format(selected_user)).executeFetchAll()
                    parameter = "Deactivated"
                    if current_status[0][0] == "F":
                        new_parameter_value, status = "T", parameter
                    else:
                        new_parameter_value, status = "F", parameter[2].upper() + parameter[3:]

                    print("User {0} will be {1}.\n".format(selected_user, status))

                self.update_parameter_record(selected_user, parameter, new_parameter_value)
                print("Successfully Updated to Database. Going back to home page.\n")
                break

    def delete_gp_patient(self):
        """
        updated table with the deleted GP record
        """
        # show all users that are deactivated for deletion
        all_deactivated_gps = SQLQuery("SELECT username FROM Users WHERE Deactivated = 'T' AND "
                                       "((UserType = 'GP') OR (UserType = 'Patient'))")
        all_deactivated_gps_result = list(all_deactivated_gps.executeFetchAll())

        if len(all_deactivated_gps_result) == 0:
            print("No deactivated GPs available to delete.\n")
            return

        # select a deactivated GP account to delete
        while True:
            all_deactivated_gps_table, _ = self.view_all_patients_and_GPs(all_deactivated_gps_result)
            selected_gp_number = Parser.selection_parser(options=all_deactivated_gps_table)
            selected_gp = all_deactivated_gps_table[selected_gp_number]
            if selected_gp == "back":
                Parser.print_clean()
                break
            else:
                # delete query, make sure to delete all presence of that user
                delete_query = SQLQuery("DELETE FROM Users WHERE username=:who")
                delete_query.executeCommit({"who": selected_gp})
                Parser.print_clean("GP {0} deleted from Users table.\n".format(selected_gp))
                break

    def view_all_patients_and_GPs(self, all_results):
        """
        :param list all_results: All results from query
        :return: List of all GPs and Patients with ID and another list with only names of patient/GP
        """
        all_gps_and_patients_table, gp_and_patient = {}, []
        for nameIndex in range(len(all_results)):
            gp_and_patient.append((nameIndex, all_results[nameIndex][0]))
            all_gps_and_patients_table[str(nameIndex+1)] = all_results[nameIndex][0]
        all_gps_and_patients_table["--back"] = "back"
        return all_gps_and_patients_table, gp_and_patient

    def update_parameter_record(self, selected_user, parameter, new_parameter_value):
        """
        :param str selected_user: Current user, admin is changing
        :param str parameter: Current table column admin is changing
        :param str new_parameter_value: New value to change within the table column of the currently selected user
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
    Admin(current_user).main_menu()

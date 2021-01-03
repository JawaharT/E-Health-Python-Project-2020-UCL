import logging
from typing import Tuple

from tabulate import tabulate

from database import SQLQuery
from encryption import EncryptionHelper
from iohandler import Parser
from main import User, MenuHelper

logger = logging.getLogger(__name__)


class Admin(User):
    """Navigate through Admin features and functionality once logged in."""

    def main_menu(self) -> None:
        """
        Main Menu for Admin-type users.
        """
        logger.info("logged in as Admin")
        while True:
            print("You're currently viewing main menu options for Admin {}.".format(self.username))
            user_input = Parser.selection_parser(
                options={"A": "View Records", "B": "Add New GP or Patient", "C": "Edit GP or Patient",
                         "D": "Delete Existing GP or Patient", "--logout": "logout"})
            if user_input == "--logout":
                logger.info("User Logged Out")
                Parser.user_quit()
            elif user_input == "A":
                self.view_records()
            elif user_input == "B":
                self.add_gp_patient()
            elif user_input == "C":
                self.edit_gp_patient()
            else:
                self.delete_gp_patient()

    def view_records(self) -> None:
        """
        User interface for viewing the desired records
        """
        while True:
            Parser.print_clean("You're logged in as {} with Administrator privileges.".format(self.username))
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
                headers = ("BookingNo", "NHSNo", "StaffID", "Timeslot", "Symptoms", "Confirmed", "Attended",
                           "Diagnosis", "Notes")
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

            logger.info("Selected table to view")
            all_data = SQLQuery(query_string).fetch_all(decrypter=EncryptionHelper(), parameters=parameters)

            if len(list(all_data)) == 0:
                logger.info("No Records to show")
                Parser.print_clean("No records Available.\n")
                # input("Press Enter to continue...")
                Parser.handle_input()
                continue

            logger.info("Show existing records to admin through pages")

            # Paging records
            start, step = 0, 2
            end = len(all_data) if len(all_data) % 2 == 0 else len(all_data) + 1

            for page_length in range(start, end, step):
                logger.info("Shown Page: " + str((page_length+2)/2))
                for row in all_data[page_length: page_length+2]:
                    current = []
                    for index, title in enumerate(headers):
                        current.append((title + ":", row[index]))
                    print(tabulate(current))

                if page_length+2 >= end:
                    break

                user_input = Parser.selection_parser(
                    options={"A": "Proceed to next page", "B": "Continue to next part"})

                if user_input == "A":
                    continue
                else:
                    break

            print("Completed operation.\n")

            logger.info("Option to edit records")
            if record_viewer == "A" or record_viewer == "B":
                user_input = Parser.selection_parser(
                    options={"A": "Proceed to editing the records", "--back": "back"})
                if user_input == "A" and user_type == "Patient":
                    self.edit_gp_patient("Patient")
                elif user_input == "A" and user_type == "GP":
                    self.edit_gp_patient("GP")
                else:
                    continue
            else:
                # input("Press Enter to continue...")
                Parser.handle_input()

    @staticmethod
    def add_gp_patient() -> None:
        """
        Update table with new GP or patient record
        """
        Parser.print_clean("You are now adding a new account as administrator. The new record will be automatically "
                           "activated.")
        # input("Press Enter to continue...")
        Parser.handle_input()
        MenuHelper().register(admin=True)

    def edit_gp_patient(self, account_types="all") -> None:
        """
        Edit existing GP or Patient Record
        """
        # show all GPs and Patients
        if account_types == "all":
            list_accounts = list(SQLQuery("SELECT username FROM Users WHERE UserType = 'GP' or "
                                          "UserType = 'Patient'").fetch_all())
        elif account_types == "GP":
            list_accounts = list(SQLQuery("SELECT username FROM Users WHERE UserType = 'GP'").fetch_all())

        elif account_types == "Patient":
            list_accounts = list(SQLQuery("SELECT username FROM Users WHERE UserType = 'Patient'").fetch_all())

        else:
            logger.warning("Incorrect input")
            print("Input incorrect...")
            return

        if len(list_accounts) == 0:
            Parser.print_clean("No user accounts matching the search criteria... Please add before coming back.\n")
            return

        # select a user from the table
        while True:
            full_accounts_table, accounts_table = self.list_accounts(list_accounts)
            selected_user_number = Parser.selection_parser(options=full_accounts_table)
            selected_user = full_accounts_table[selected_user_number]
            if selected_user == "back":
                Parser.print_clean()
                break
            else:
                logger.info("Edit " + account_types + " Users")
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
                elif record_editor == "A":
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
                                              .format(selected_user)).fetch_all()
                    parameter = "Deactivated"
                    if current_status[0][0] == "F":
                        new_parameter_value, status = "T", parameter
                    else:
                        new_parameter_value, status = "F", parameter[2].upper() + parameter[3:]

                    print("User {0} will be {1}.\n".format(selected_user, status))

                logger.info("Admin edited " + parameter + " of " + selected_user)
                self.update_parameter_record(selected_user, parameter, new_parameter_value)
                print("Successfully Updated to Database. Going back to home page.\n")
                break

    def delete_gp_patient(self) -> bool:
        """
        updated table with the deleted GP record
        """
        # show all users that are deactivated for deletion
        all_deactivated_users = SQLQuery("SELECT username FROM Users WHERE Deactivated = 'T' AND "
                                         "((UserType = 'GP') OR (UserType = 'Patient'))")
        all_deactivated_users_result = list(all_deactivated_users.fetch_all())

        if len(all_deactivated_users_result) == 0:
            Parser.print_clean("For safety, you can only delete accounts which are currently deactivated. To remove "
                               "an active account, deactivate it first.")
            print("No deactivated GPs available to delete.\n")
            return False

        # select a deactivated GP/Patient account to delete
        while True:
            all_deactivated_users_table, _ = self.list_accounts(all_deactivated_users_result)
            selected_user_number = Parser.selection_parser(options=all_deactivated_users_table)
            selected_user = all_deactivated_users_table[selected_user_number]
            if selected_user == "--back":
                return False
            else:
                logger.info("Selected GP/ Patient account to delete")
                # delete query, make sure to delete all presence of that user
                logger.info("Removed selected " + selected_user + " from Users table")
                delete_query1 = SQLQuery("DELETE FROM Users WHERE username=:who")
                delete_query1.commit({"who": selected_user})
                print("GP {0} deleted from Users table.\n".format(selected_user))
                Parser.print_clean()
                return True

    @staticmethod
    def list_accounts(all_results) -> Tuple[dict, list]:
        """
        :param list all_results: All results from query
        :return: Tuple[list,list]: dict with all GPs and Patients with ID and another list with only names of patient/GP
        """
        full_accounts_table, accounts_table = {}, []
        for nameIndex in range(len(all_results)):
            accounts_table.append((nameIndex, all_results[nameIndex][0]))
            full_accounts_table[str(nameIndex + 1)] = all_results[nameIndex][0]
        full_accounts_table["--back"] = "back"
        return full_accounts_table, accounts_table

    @staticmethod
    def update_parameter_record(selected_user, parameter, new_parameter_value) -> bool:
        """
        :param str selected_user: Current user, admin is changing
        :param str parameter: Current table column admin is changing
        :param str new_parameter_value: New value to change within the table column of the currently selected user
        """
        try:
            SQLQuery("UPDATE Users SET {0} = ? WHERE username = ?".format(parameter)).commit((new_parameter_value,
                                                                                              selected_user))
            logger.info("Updated record in database")
            return True
        except Exception:
            logger.debug("Unexpected database error")
            return False

    def first_login(self):
        """
        Placeholder function to maintain consistent structure with Patient and GP classes
        :return: True
        """
        return True


if __name__ == "__main__":
    current_user = MenuHelper.login()
    MenuHelper.dispatcher(current_user["username"], current_user["user_type"])
    Admin(current_user).main_menu()

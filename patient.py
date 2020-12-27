from tabulate import tabulate
from main import User, MenuHelper
from encryption import EncryptionHelper
from database_help import SQLQuery
from parser_help import Parser
import datetime
import sys




class Patient(User):
    """Navigate through Patient features."""

    def main_menu(self):
        """
        Main Menu for Patient-type users.
        """
        while True:
            user_input = Parser.selection_parser(
                options={"A": "Book Appointments", "B": "Cancel Appointments", "C": "Rate Your Appointment",
                         "D": "Review Appointments", "--logout": "logout"})
            if user_input == "--logout":
                Parser.user_quit()
            elif user_input == "A":
                self.booking_appointment()
            elif user_input == "B":
                self.cancel_appointment()
            elif user_input == "C":
                self.rate_appointment()
            else:
                self.review_appointment()


    def booking_appointment(self):
        pass

    def cancel_appointment(self):
        pass

    def rate_appointment(self):
        pass

    def review_appointment(self):

        while True:
            record_viewer = Parser.selection_parser(
                options={"A": "Review Appointments", "B": "Review Prescriptions",
                         "--back": "back"})

            if record_viewer == "--back":
                Parser.print_clean("\n")
                return
            elif record_viewer == "A":
                query_string = "SELECT visit.BookingNo, visit.NHSNo, users.firstName, users.lastName, " \
                               "visit.Timeslot, visit.PatientInfo, visit.Confirmed, visit.Attended,visit.Rating " \
                               "FROM visit INNER JOIN users ON " \
                               "visit.NHSNo = users.ID WHERE visit.NHSNo = ? "
                headers = ("BookingNo", "NHSNo", "Firstname", "Lastname", "Timeslot",
                           "PatientInfo", "Confirmed", "Attended", "Rating")

            else:
                query_string = "SELECT prescription.BookingNo, users.ID, users.firstName, users.lastName, " \
                               "visit.PatientInfo, visit.Diagnosis, prescription.drugName, prescription.quantity, " \
                               "prescription.Instructions, visit.Notes " \
                               "FROM ((visit INNER JOIN users ON visit.NHSNo = users.ID)" \
                               "INNER JOIN prescription ON visit.BookingNo = prescription.BookingNo" \
                               "WHERE visit.NHSNo = ? "
                headers = ("BookingNo", "NHSNo", "Firstname", "Lastname", "PatientInfo", "Diagnosis",
                           "DrugName", "Quantity", "Instructions", "Notes")

            query = SQLQuery(query_string)
            all_data = query.executeFetchAll(decrypter=EncryptionHelper(), parameters=(self.ID))

            if len(list(all_data)) == 0:
                Parser.print_clean("No records Available.\n")
            else:
                Parser.print(tabulate(all_data, headers))


if __name__ == "__main__":
    current_user = MenuHelper.login()
    MenuHelper.dispatcher(current_user["username"], current_user["user_type"])
    Patient(current_user).main_menu()

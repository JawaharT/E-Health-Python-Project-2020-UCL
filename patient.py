from tabulate import tabulate
from main import User, MenuHelper
from encryption import EncryptionHelper
from iohandler import Parser
from database import SQLQuery
#from typing import Union
import datetime

from exceptions import DBRecordError
import logging
logger = logging.getLogger(__name__)
#this need to be changed
print_clean = Parser.print_clean
delta = datetime.timedelta


class Patient(User):
    """
    patient Class with navigation options and various functionalities.
    """
    def main_menu(self) -> None:
        """
        Main Menu for Patient-type users.
        """
        logger.info("logged in as Patient")
        while True:
            print("You're currently viewing main menu options for Patient {}.".format(self.username))
            option_selection = Parser.selection_parser(
                options={"B": "book appointments", "I": "view /check in unattended appointment",
                         "C": "cancel appointment", "R": "review/rate appointments",
                         "--logout": "Logout"})
            if option_selection == "--logout":
                # Quitting is required for logout to ensure all personal data is cleared from session
                logger.info("User Logged Out")
                Parser.user_quit()
            elif option_selection == "B":
                booking_selection = Parser.selection_parser(options={"G": "select by GP number", "D": "select by date"})
                if booking_selection == "D":
                    self.book_appointment_date()
                elif booking_selection == "G":
                    self.book_appointment_GP()
                elif booking_selection == "--back":
                    continue
            elif option_selection == "I":
                self.check_in_appointment()
            elif option_selection == "C":
                self.cancel_appointment()
            elif option_selection == "R":
                r_selection = Parser.selection_parser(options={"A": "review", "B": "rate", "--back": "back"})
                if r_selection == "--back":
                    continue
                elif r_selection == "A":
                    self.review_appointment()
                elif r_selection == "B":
                    self.rate_appointment()

    def book_appointment_date(self) -> bool:
        """
        choose a date -- choose a GP
        --choose time
        --give random number as bookingNo
        --move from available_time
        --insert in visit
        """
        stage = 0
        while True:
            while stage == 0:
                # choose a date
                selected_date = Parser.date_parser(question=f"Booking appointments for Patient {self.username}.")
                print(selected_date)
                if selected_date == "--back":
                    print_clean()
                    return False
                # show available GP
                gp_result_raw = SQLQuery("SELECT ID, firstName, lastName, Timeslot FROM (available_time JOIN Users on "
                                     "available_time.StaffID = Users.ID) WHERE Timeslot >= ? AND Timeslot <= ?"
                                     ).fetch_all(decrypter=EncryptionHelper(),
                                                 parameters=(selected_date, selected_date + delta(days=1)))

                gp_numbers = []
                gp_table = []
                gp_pointer = 0
                for result in gp_result_raw:
                    gp_numbers.append(result[0])
                    result.pop(0)
                    gp_pointer += 1
                    gp_table.append([gp_pointer, result[0], result[1], result[2]])
                print(f"You are viewing all available appointments for: {selected_date}")
                if len(gp_table) == 0:
                    print("There are no available appointments for this day.")
                    stage = 0
                    # input("Press Enter to continue...")
                    Parser.handle_input()
                else:
                    stage = 1

            while stage == 1:
                # show list of time
                print(tabulate(gp_table, headers=["Pointer", "GP First Name", "GP Last Name", "Timeslot"]))
                selected_gp_pointer = Parser.list_number_parser("Select appointment by Pointer:",
                                                                 (1, len(gp_table)), allow_multiple=False)
                if selected_gp_pointer == '--back':
                    return False
                selected_appointment = gp_table[selected_gp_pointer - 1]
                gp_number = gp_numbers[selected_gp_pointer - 1]
                stage = 2

            while stage == 2:
                print("This is the time slot which will be booked by you:")
                print(tabulate([selected_appointment], headers=["Pointer", "GP First Name", "GP Last Name", "Timeslot"]))
                confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})
                # Confirm if user wants to confirm booking
                if confirm == "Y":
                    try:
                        SQLQuery("INSERT INTO visit (NHSNo, StaffID, Timeslot, Confirmed)"
                                 "VALUES (?, ?, ?, ?)"
                                 ).commit((self.ID, gp_number, selected_appointment[3], "P"))
                        SQLQuery("DELETE FROM available_time WHERE StaffID = ? AND Timeslot = ?"
                                 ).commit((gp_number, selected_appointment[3]))
                        print("Booking successful!")
                        visit_result = SQLQuery("SELECT BookingNo, NHSNo, StaffID, Timeslot FROM visit "
                                                "WHERE StaffID = ? AND Timeslot = ?"
                                                ).fetch_all(parameters=(gp_number,selected_appointment[3]))
                        print(tabulate(visit_result, headers=["bookingNo", "NHSNo", "GP", "Timeslot"]))
                        stage = 3
                        # input("Press Enter to continue...")
                        Parser.handle_input()
                    except DBRecordError:
                        print("Error encountered")
                        # input("Press Enter to continue...")
                        Parser.handle_input()
                if confirm == "N":
                    print("Booking cancelled.")
                    slots_to_remove = []
                    # input("Press Enter to continue...")
                    Parser.handle_input()
                while stage == 3:
                    print_clean()
                    info_input = Parser.string_parser(
                        "Please input your primary complaint before the appointment: ")
                    SQLQuery(" UPDATE Visit SET PatientInfo = ? WHERE StaffID = ? AND Timeslot = ? "
                             ).commit((info_input, gp_number, selected_appointment[3]))
                    Parser.print_clean("Your description have been recorded successfully!")
                    # input("Press Enter to continue...")
                    Parser.handle_input()
                    return True

    def check_in_appointment(self):
        """
        show all booking
        if time later, allow to check in
        change attend to T
        """
        stage = 0
        while True:
            while stage == 0:
                print("This is time slot booked by you:")
                patient_appointment_result = SQLQuery(
                    "SELECT bookingNo, NHSNo, StaffID, Timeslot, Confirmed FROM visit "
                    "WHERE NHSNo = ? AND Attended = ? ",
                ).fetch_all(parameters=(self.ID, "F"))

                patient_confirmed_appointment_table = []
                patient_unconfirmed_appointment_table = []

                j = 0
                for i in range(len(patient_appointment_result)):

                    if patient_appointment_result[i][4] == "T":
                        patient_confirmed_appointment_table.append([i + 1, str(patient_appointment_result[i][0]),
                                                                    str(patient_appointment_result[i][1]),
                                                                    str(patient_appointment_result[i][2]),
                                                                    str(patient_appointment_result[i][3]),
                                                                    str(patient_appointment_result[i][4])])
                    elif patient_appointment_result[i][4] == "F":
                        # j = j + 1
                        patient_unconfirmed_appointment_table.append([j + 1, str(patient_appointment_result[i][0]),
                                                                      str(patient_appointment_result[i][1]),
                                                                      str(patient_appointment_result[i][2]),
                                                                      str(patient_appointment_result[i][3]),
                                                                      str(patient_appointment_result[i][4])])
                        j = j + 1
                    else:
                        print("error")

                print(f"You are viewing all your unattended appointment: ")

                if len(patient_confirmed_appointment_table) == 0 and len(patient_unconfirmed_appointment_table) == 0:
                    print(f"You don't have any unattended appointment")
                    # input("Press Enter to continue...")
                    Parser.handle_input()
                    stage = 0

                if len(patient_confirmed_appointment_table) != 0:
                    print(f"These are appointments already confirmed by GP")
                    print("\n")
                    print(tabulate(patient_confirmed_appointment_table,
                                   headers=["pointer", "bookingNo", "NHSNo", "staffID", "timeslot", "confirmed"]))

                if len(patient_unconfirmed_appointment_table) != 0:
                    print(f"These appointment have not been confirmed by GP, please wait or change your appointment ")
                    print("\n")
                    print(tabulate(patient_unconfirmed_appointment_table,
                                   headers=["pointer", "bookingNo", "NHSNo", "staffID", "timeslot", "confirmed"]))

                option_selection = Parser.selection_parser(
                    options={"I": "check in confirmed appointment", "C": "change appointment", "--back": "back"})
                if option_selection == "--back":
                    return
                elif option_selection == "C":
                    return
                elif option_selection == "I":
                    stage = 1

            while stage == 1:
                print(f"These are your unattended appointments ")
                print("\n")
                print(tabulate(patient_confirmed_appointment_table,
                               headers=["pointer", "bookingNo", "NHSNo", "staffID", "timeslot", "confirmed"]))
                print("\n")

                print("please check in after your attending")
                print("do you want to edit one or edit more at once?")
                # option_selection = Parser.selection_parser(options={"E": "one change", "M": "more than one change","--back": "back"})
                # if option_selection == "--back":
                #     return
                # elif option_selection == "E":
                #     selected_appointment = Parser.pick_pointer_parser("Select an appointment by the Pointer.",
                #                                                       (1, len(patient_confirmed_appointment_table)))

                # elif option_selection == "M":
                selected_appointment = Parser.list_number_parser("Select an appointment by the Pointer.",
                                                                 (1, len(patient_confirmed_appointment_table)))

                if selected_appointment == '--back':
                    return
                appointment_to_check_in = []
                for row in patient_confirmed_appointment_table:
                    if row[0] in selected_appointment:
                        appointment_to_check_in.append(row[1])

                confirm = Parser.selection_parser(options={"Y": "check in", "N": "Go back"})
                if confirm == "Y":
                    try:
                        for appointment in appointment_to_check_in:
                            SQLQuery(" UPDATE Visit SET Attended = ? WHERE BookingNo = ? "
                                     ).commit(("T", appointment))

                        print("check in successfully.")
                        # input("Press Enter to continue...")
                        Parser.handle_input()
                        return True
                    # temporary exception
                    except DBRecordError:
                        print("Error encountered")
                        slots_to_remove = []
                        # input("Press Enter to continue...")
                        Parser.handle_input()
                if confirm == "N":
                    print("Removal cancelled.")
                    slots_to_remove = []
                    # input("Press Enter to continue...")
                    Parser.handle_input()

    def cancel_appointment(self):
        """
        bookings can be cancelled five days in advance
        move from visit
        insert in available time
        """
        stage = 0
        while True:
            while stage == 0:
                logger.info("Selected all appointments can be cancelled")
                query_string = "SELECT BookingNo, NHSNo, StaffID, Timeslot, PatientInfo" \
                               "FROM visit  WHERE NHSNo = ? AND Timeslot >= ? "
                all_valid_cancel = SQLQuery(query_string)
                all_valid_cancel_result = all_valid_cancel.fetch_all(
                    parameters=(self.ID, datetime.datetime.now() + datetime.timedelta(days=5)))
                cancel_table = []
                cancel_table_raw = []
                cancel_pointer = []

                for i in range(len(all_valid_cancel_result)):
                    cancel_table.append([i + 1, str(all_valid_cancel_result[i][0]), str(all_valid_cancel_result[i][1]),
                                         str(all_valid_cancel_result[i][2]), str(all_valid_cancel_result[i][3]),
                                         str(all_valid_cancel_result[i][4])])
                    cancel_table_raw.append([i + 1, all_valid_cancel_result[i][0], all_valid_cancel_result[i][1],
                                             all_valid_cancel_result[i][2], all_valid_cancel_result[i][3],
                                             all_valid_cancel_result[i][4]])
                    cancel_pointer.append(i + 1)
                print(f"You are viewing all the appointments can be cancelled.")
                if len(cancel_table) == 0:
                    logger.info("No Records to show")
                    print(f"No Appointments can be cancelled.\n")
                    return
                else:
                    stage = 1

            while stage == 1:
                logger.info("View all appointments that can be cancelled")
                print(tabulate(cancel_table, headers=["Pointer", "BookingNo", "NHSNo",
                                                      "StaffID", "Timeslot", "PatientInfo"]))
                selected_cancel_appointment = Parser.pick_pointer_parser("Select an appointment "
                                                                         "to cancel by the Pointer.",
                                                                         (1, len(cancel_table)))

                selected_row = cancel_table[selected_cancel_appointment - 1]
                selected_row_raw = cancel_table_raw[selected_cancel_appointment - 1]

                print("This is appointment you want to cancel:")
                print(tabulate([selected_row], headers=["Pointer", "BookingNo", "NHSNo",
                                                        "StaffID", "Timeslot", "PatientInfo"]))

                confirmation = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})
                if confirmation == "Y":
                    SQLQuery("DELETE FROM visit WHERE BookingNo = ? "
                             ).commit(parameters=(selected_row_raw[1]))
                    SQLQuery("INSERT INTO available_time VALUES (?,?)"
                             ).commit(parameters=(selected_row_raw[3], selected_row_raw[4]))
                    print("Appointment is cancelled successfully.")

                    visit_result = SQLQuery("SELECT bookingNo, NHSNo, StaffID, Timeslot, PatientInfo FROM visit "
                                            "WHERE NHSNo = ? AND Timeslot >= ? "
                                            ).fetch_all(
                        parameters=(self.ID, datetime.datetime.now() + datetime.timedelta(days=5)))

                    print(tabulate(visit_result, headers=["bookingNo", "NHSNo", "GP", "Timeslot", "PatientInfo"]))

                else:
                    logger.info("Go back and select again")
                    Parser.print_clean()
                    return

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
                               "visit.PatientInfo, visit.Diagnosis, visit.Notes, prescription.drugName, " \
                               "prescription.quantity, prescription.Instructions " \
                               "FROM (visit INNER JOIN users ON visit.NHSNo = users.ID) " \
                               "INNER JOIN prescription ON " \
                               "visit.BookingNo = prescription.BookingNo WHERE visit.NHSNo = ? "

                headers = ("BookingNo", "NHSNo", "Firstname", "Lastname", "PatientInfo", "Diagnosis",
                           "DrugName", "Quantity", "Instructions", "Notes")
            logger.info("Selected table to view")
            query = SQLQuery(query_string)
            all_data = query.fetch_all(decrypter=EncryptionHelper(), parameters=(self.ID,))

            if len(list(all_data)) == 0:
                logger.info("No Records to show")
                Parser.print_clean("No records Available.\n")
            else:
                print(tabulate(all_data, headers))

    def rate_appointment(self):
        while True:
            stage = 0
            while True:
                while stage == 0:

                    patient_result = SQLQuery(
                        "SELECT bookingNo, StaffID, Timeslot FROM visit "
                        "WHERE NHSNo = ? AND Attended = ? ",
                    ).fetch_all(parameters=(self.ID, "T"))

                    patient_attended_appointment_table = []
                    # patient_unconfirmed_appointment_table_raw = []
                    if len(patient_result) == 0:
                        print(f"You don't have any attended appointment")
                        # input("Press Enter to back...")
                        Parser.handle_input("Press Enter to back...")
                        return
                    else:
                        for i in range(len(patient_result)):
                            patient_attended_appointment_table.append([i + 1, str(patient_result[i][0]),
                                                                       str(patient_result[i][1]),
                                                                       str(patient_result[i][2])])
                        print("This is appointments attended by you:")
                        print(tabulate(patient_attended_appointment_table,
                                       headers=["pointer", "bookingNo", "staffID", "timeslot"]))

                        print("We think highly of your feelings, please give a rate to your GP")

                        selected_rate_appointment = Parser.pick_pointer_parser("Select an appointment "
                                                                               "to cancel by the Pointer.",
                                                                               (1, len(
                                                                                   patient_attended_appointment_table)))

                        selected_row = patient_attended_appointment_table[selected_rate_appointment - 1]

                        print("This is the appointment you want to rate:")
                        print(tabulate([selected_row], headers=["Pointer", "BookingNo", "NHSNo",
                                                                "StaffID", "Timeslot", "PatientInfo"]))

                        rate_selection = Parser.selection_parser(options={"Y": "Rate", "N": "Go back"})

                        if rate_selection == "N":
                            return
                        elif rate_selection == "Y":
                            selected_rate = Parser.pick_pointer_parser("Select form 1 - 5 ", (1, 5))
                            SQLQuery(" UPDATE Visit SET Rating = ? WHERE BookingNo = ? "
                                     ).commit((selected_rate, selected_row[1]))

                            print("Your rate have been recorded successfully!")
                            Parser.string_parser("Press Enter to continue...")
                            return


if __name__ == "__main__":
    current_user = MenuHelper.login()
    MenuHelper.dispatcher(current_user["username"], current_user["user_type"])
    Patient(current_user).main_menu()

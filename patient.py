from tabulate import tabulate
from main import User, MenuHelper
from encryption import EncryptionHelper
from iohandler import Parser
from database import SQLQuery
import datetime
from exceptions import DBRecordError

print_clean = Parser.print_clean
delta = datetime.timedelta
date_now = datetime.datetime.now().date()


class Patient(User):
    """
    patient Class with navigation options and various functionalities.
    """

    def main_menu(self) -> None:
        """
        Main Menu for Patient-type users.
        """
        while True:
            print("You're currently viewing main menu options for Patient {}.".format(self.username))
            option_selection = Parser.selection_parser(
                options={"B": "book appointments", "I": "view /check in unattended appointment",
                         "C": "cancel appiontment", "R": "review/rate appointments",
                         "--logout": "Logout"})
            if option_selection == "--logout":
                # Quitting is required for logout to ensure all personal data is cleared from session
                print_clean("Logging you out...")
                Parser.user_quit()
            elif option_selection == "B":
                self.book_appointment_start()
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

    def book_appointment_start(self):
        """
        choose a date -- choose a GP
        --choose time
        --give random number as bookingNo
        --move from available_time
        --insert in visit
        """
        while True:
            result_table = self.fetch_format_appointments(date_now + delta(days=1), 8)
            Parser.print_clean("You are viewing all available appointments for the next week. To view appointments up "
                               "to 2 weeks ahead, use 'select by date' or 'select by GP' options below")
            if not result_table:
                return False
            print(tabulate([result[0:4] for result in result_table], headers=["Pointer", "GP Name", "Last Name",
                                                                              "Timeslot"]))
            print("How would you like to choose? ")
            booking_selection = Parser.selection_parser(
                options={"E": "select earliest available appointment",
                         "G": "select by GP", "D": "select by date", "--back": "back"})
            if booking_selection == "E":
                if self.process_booking(result_table[0]):
                    return True
            if booking_selection == "D":
                if self.book_appointment_date():
                    return True
            elif booking_selection == "G":
                if self.book_appointment_gp():
                    return True
            elif booking_selection == "--back":
                Parser.print_clean()
                return False

    @staticmethod
    def fetch_format_appointments(selected_date, selected_delta=1, GP_ID='%'):
        result = SQLQuery("SELECT firstName, lastName, Timeslot, available_time.StaffID FROM "
                          "(available_time JOIN Users ON available_time.StaffID = Users.ID) WHERE "
                          "available_time.StaffID LIKE ? AND Timeslot >= ? AND Timeslot <= ? ORDER BY Timeslot"
                          ).fetch_all(parameters=(GP_ID, selected_date, selected_date + delta(days=selected_delta)),
                                      decrypter=EncryptionHelper())
        if len(result) == 0:
            print(f"There are no available appointments matching the search criteria. ")
            Parser.handle_input("Press Enter to continue.")
            return False
        result_table = []
        for count, item in enumerate(result):
            result_table.append([count + 1, item[0], item[1], item[2], item[3]])
        return result_table

    def book_appointment_date(self):
        while True:
            selected_date = Parser.date_parser(question=f"Managing for Patient {self.username}.\n"
                                                        "Select a Date:\n")
            if selected_date == "--back":
                print_clean()
                return False
            result_table = self.fetch_format_appointments(selected_date)
            if not result_table:
                continue
            print(f"You are viewing all available appointments for: {selected_date}")
            print(tabulate([result[0:4] for result in result_table], headers=["Pointer", "GP Name", "Last Name",
                                                                              "Timeslot"]))
            selected_appointment = Parser.list_number_parser("Select an appointment by the Pointer.",
                                                             (1, len(result_table)), allow_multiple=False)
            if selected_appointment == '--back':
                return False
            selected_row = result_table[selected_appointment - 1]
            if self.process_booking(selected_row):
                return True

    def book_appointment_gp(self):
        while True:
            gp_result = SQLQuery("SELECT users.firstName, users.lastName, GP.Introduction, GP.ClinicAddress, "
                                 "GP.ClinicPostcode, GP.Gender, GP.Rating, users.ID FROM (GP INNER JOIN users ON "
                                 "GP.ID = users.ID) WHERE users.ID IN ( SELECT DISTINCT StaffID FROM available_time "
                                 "WHERE Timeslot >= ? AND Timeslot <= ? )"
                                 ).fetch_all(parameters=(date_now + delta(days=1), date_now + delta(days=15)),
                                             decrypter=EncryptionHelper())
            gp_table = []
            for count, item in enumerate(gp_result):
                gp_table.append([count + 1, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]])
            if len(gp_table) == 0:
                print("There are no GPs in the system yet.")
                Parser.handle_input("Press Enter to continue...")
                return False
            Parser.print_clean(f"You are viewing all available GPs in 2 weeks from: {date_now} ")
            print(tabulate([gp[0:8] for gp in gp_table], headers=["Pointer", "First Name", "Last Name", "Introduction",
                                                                  "Clinic Address", "Clinic Postcode",
                                                                  "Gender", "Rating"]))
            selected_gp_pointer = Parser.list_number_parser("Select GP by the Pointer.",
                                                            (1, len(gp_table)), allow_multiple=False)
            if selected_gp_pointer == '--back':
                return False
            selected_gp = gp_table[selected_gp_pointer - 1][8]
            result_table = self.fetch_format_appointments(date_now + delta(days=1), 15, selected_gp)
            if not result_table:
                continue
            print(f"You are viewing appointments for the selected GP:")
            print(tabulate([result[0:4] for result in result_table], headers=["Pointer", "GP First Name",
                                                                              "Last Name", "Timeslot"]))
            selected_appointment = Parser.list_number_parser("Select an appointment by the Pointer.",
                                                             (1, len(result_table)), allow_multiple=False)
            if selected_appointment == '--back':
                return False
            selected_row = result_table[selected_appointment - 1]
            if self.process_booking(selected_row):
                return True

    def process_booking(self, selected_row):
        encrypt = EncryptionHelper().encrypt_to_bits
        while True:
            Parser.print_clean("This is time slot will be booked by you:")
            print("GP: {} {}".format(selected_row[1], selected_row[2]))
            print("Timeslot: {}\n".format(selected_row[3]))
            confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})
            # Confirm if user wants to delete slots
            if confirm == "Y":
                try:
                    SQLQuery("BEGIN TRANSACTION; INSERT INTO Visit (NHSNo, StaffID, Timeslot, Confirmed, Attended) "
                             f"VALUES ({self.ID}, '{selected_row[4]}', '{selected_row[3]}', 'P', 'F'); "
                             f"DELETE FROM available_time WHERE StaffID = '{selected_row[4]}'"
                             f" AND TIMESLOT = '{selected_row[3]}'; COMMIT"
                             ).commit(multiple_queries=True)
                    print("Booked successfully.")
                    visit_result = SQLQuery("SELECT BookingNo, NHSNo, firstName, lastName, Timeslot FROM "
                                            "(Visit JOIN Users ON VISIT.StaffID = Users.ID)"
                                            "WHERE Timeslot = ? AND StaffID = ? "
                                            ).fetch_all(parameters=(selected_row[3], selected_row[4]),
                                                        decrypter=EncryptionHelper())
                    booking_no = visit_result[0][0]
                    print(tabulate(visit_result,
                                   headers=["BookingNo", "NHSNo", "GP First Name", "Last Name", "Timeslot"]))
                    Parser.handle_input("Press Enter to continue...")
                except DBRecordError:
                    print("Error encountered")
                    Parser.handle_input("Press Enter to continue...")
                    return False
                info_input = encrypt(Parser.string_parser("Please enter your main complaint before the visit: "))
                SQLQuery("UPDATE Visit SET PatientInfo = ? WHERE BookingNo = ? "
                         ).commit((info_input, booking_no))
                print("Your information have been recorded successfully!")
                Parser.handle_input("Press Enter to continue...")
                Parser.print_clean()
                return True
            else:
                print("Booking cancelled.")
                Parser.handle_input("Press Enter to continue...")
                Parser.print_clean()
                return False

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
                patient_rejected_appointment_table = []

                j = 0
                r = 0
                for i in range(len(patient_appointment_result)):

                    if patient_appointment_result[i][4] == "T":
                        patient_confirmed_appointment_table.append([i + 1, str(patient_appointment_result[i][0]),
                                                                    str(patient_appointment_result[i][1]),
                                                                    str(patient_appointment_result[i][2]),
                                                                    str(patient_appointment_result[i][3]),
                                                                    str(patient_appointment_result[i][4])])

                    elif patient_appointment_result[i][4] == "P":
                        patient_unconfirmed_appointment_table.append([j + 1, str(patient_appointment_result[i][0]),
                                                                      str(patient_appointment_result[i][1]),
                                                                      str(patient_appointment_result[i][2]),
                                                                      str(patient_appointment_result[i][3]),
                                                                      str(patient_appointment_result[i][4])])
                        j = j + 1
                    elif patient_appointment_result[i][4] == "F":
                        patient_rejected_appointment_table.append([r + 1, str(patient_appointment_result[i][0]),
                                                                   str(patient_appointment_result[i][1]),
                                                                   str(patient_appointment_result[i][2]),
                                                                   str(patient_appointment_result[i][3]),
                                                                   str(patient_appointment_result[i][4])])
                        r = r + 1
                    else:
                        print("error")

                print(f"You are viewing all your booked appointments: ")

                if len(patient_confirmed_appointment_table) == 0 and len(patient_unconfirmed_appointment_table) == 0 \
                        and len(patient_rejected_appointment_table) == 0:
                    print(f"You have not booked any appointment")
                    input("Press Enter to back...")
                    return

                if len(patient_confirmed_appointment_table) != 0:
                    print(f"These are appointments already confirmed by GP")
                    print(tabulate(patient_confirmed_appointment_table,
                                   headers=["pointer", "bookingNo", "NHSNo", "staffID", "timeslot", "confirmed"]))

                if len(patient_unconfirmed_appointment_table) != 0:
                    print(f"These appointment are pending, please wait or change your appointment ")
                    print(tabulate(patient_unconfirmed_appointment_table,
                                   headers=["pointer", "bookingNo", "NHSNo", "staffID", "timeslot", "confirmed"]))

                if len(patient_rejected_appointment_table) != 0:
                    print(f"These appointment have been rejected by GP, please wait or change your appointment ")
                    print(tabulate(patient_rejected_appointment_table,
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

                if len(patient_confirmed_appointment_table) == 0:
                    print(f"You don't have any unattended appointment")
                    input("Press Enter to back...")
                    return

                print(f"These are your unattended appointments ")
                print(tabulate(patient_confirmed_appointment_table,
                               headers=["pointer", "bookingNo", "NHSNo", "staffID", "timeslot", "confirmed"]))
                print("please check in after your attending")

                selected_appointment = Parser.list_number_parser("Select an appointment by the Pointer.",
                                                                 (1, len(patient_confirmed_appointment_table)))

                if selected_appointment == '--back':
                    return

                appointment_to_check_in = []

                for row in patient_confirmed_appointment_table:
                    if row[0] in selected_appointment:
                        appointment_date = datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
                        if appointment_date <= datetime.datetime.now():
                            appointment_to_check_in.append([row[0], row[1], row[2], row[3], row[4]])
                        else:
                            print("Sorry, you can not check in before your appointment")
                            print(f"check in for: {row[4]} failed")

                if len(appointment_to_check_in) == 0:
                    print(f"There is no appointment can be checked in")
                    input("Press Enter to continue...")
                    stage = 1
                else:

                    print(f"These are your appointments selected to check in")
                    print("\n")
                    print(tabulate(appointment_to_check_in,
                                   headers=["pointer", "bookingNo", "NHSNo", "staffID", "timeslot", "confirmed"]))
                    print("\n")

                    confirm = Parser.selection_parser(options={"Y": "check in", "N": "Go back"})
                    if confirm == "Y":
                        try:
                            for appointment in appointment_to_check_in:
                                SQLQuery(" UPDATE Visit SET Attended = ? WHERE BookingNo = ? "
                                         ).commit(("T", appointment[1]))

                            print("check in successfully.")
                            input("Press Enter to continue...")
                            return True
                        # temporary exception
                        except DBRecordError:
                            print("Error encountered")
                            slots_to_remove = []
                            input("Press Enter to continue...")
                    if confirm == "N":
                        print("Removal cancelled.")
                        slots_to_remove = []
                        input("Press Enter to continue...")

    def cancel_appointment(self):
        """
            bookings can be cancelled five days in advance
            move from visit
            insert in available time
            """
        stage = 0
        while True:
            while stage == 0:
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
                    print(f"No Appointments can be cancelled.\n")
                    return
                else:
                    stage = 1

            while stage == 1:
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

            query = SQLQuery(query_string)
            all_data = query.fetch_all(decrypter=EncryptionHelper(), parameters=(self.ID,))

            if len(list(all_data)) == 0:
                Parser.print_clean("No records Available.\n")
            else:
                print(tabulate(all_data, headers))

    def rate_appointment(self):
        while True:
            stage = 0
            while True:
                while stage == 0:
                    patient_result = SQLQuery(
                        "SELECT bookingNo, StaffID, Timeslot, Rating FROM visit "
                        "WHERE NHSNo = ? AND Attended = ? ",
                    ).fetch_all(parameters=(self.ID, "T"))

                    patient_attended_appointment_table = []
                    # patient_unconfirmed_appointment_table_raw = []
                    if len(patient_result) == 0:
                        print(f"You don't have any attended appointment")
                        input("Press Enter to back...")
                        return
                    else:
                        for i in range(len(patient_result)):
                            patient_attended_appointment_table.append([i + 1, str(patient_result[i][0]),
                                                                       str(patient_result[i][1]),
                                                                       str(patient_result[i][2]),
                                                                       str(patient_result[i][3])])

                        print("There are appointments attended by you:")
                        print(tabulate(patient_attended_appointment_table,
                                       headers=["pointer", "bookingNo", "staffID", "timeslot", "rating"]))

                        print("We think highly of your feelings, please give a rate to your GP")

                        selected_rate_appointment = Parser.pick_pointer_parser(
                            "Select an appointment to rate by the Pointer.",
                            (1, len(patient_attended_appointment_table)))
                        if selected_rate_appointment == "--back":
                            print_clean()
                            return

                        selected_row = patient_attended_appointment_table[selected_rate_appointment - 1]

                        print("This is the appointment you want to rate:")
                        print(
                            tabulate([selected_row], headers=["pointer", "bookingNo", "staffID", "timeslot", "rating"]))

                        rate_selection = Parser.selection_parser(options={"Y": "Rate", "N": "Go back"})

                        if rate_selection == "N":
                            return
                        elif rate_selection == "Y":
                            try:
                                selected_rate = Parser.pick_pointer_parser("Select form 0 - 5 ", (0, 5))

                                SQLQuery(" UPDATE Visit SET Rating = ? WHERE BookingNo = ? "
                                         ).commit((selected_rate, selected_row[1]))

                                gp_rate_result = SQLQuery("SELECT Rating FROM visit WHERE StaffID = ? AND Attended = ?"
                                                          ).fetch_all(parameters=(selected_row[2], "T"))

                                gp_rate_num = 0

                                # print(gp_rate_result)
                                if gp_rate_result != 0:
                                    cont = 0
                                    for i in range(len(gp_rate_result)):
                                        # print(type(gp_rate_result[i][0]))
                                        if type(gp_rate_result[i][0]) is int:
                                            # print(gp_rate_result[i][0])
                                            cont += 1
                                            gp_rate_num = gp_rate_num + gp_rate_result[i][0]

                                    # print(cont)
                                    gp_rate_average = round((gp_rate_num / cont), 2)
                                    # print(gp_rate_average)
                                    try:

                                        SQLQuery(" UPDATE GP SET Rating = ? WHERE ID = ? "
                                                 ).commit((gp_rate_average, selected_row[2]))
                                        print("Your rate have been recorded successfully!")
                                    except DBRecordError:
                                        print("Error encountered")
                                        input("Press Enter to continue...")

                                else:
                                    gp_rate_num = selected_rate
                                    # print(gp_rate_num )
                                    SQLQuery(" UPDATE gp SET Rating = ? WHERE ID = ? "
                                             ).executeCommit((gp_rate_num, selected_row[2]))
                                    print("Your rate have been recorded successfully!")

                                input("Press Enter to continue...")
                                stage = 0
                            except DBRecordError:
                                print("Error encountered")
                                input("Press Enter to continue...")

    def first_login(self):
        Parser.print_clean("Welcome Patient {}. This is your first login. ".format(self.username))
        print("You need to input additional information before you can proceed.")
        Parser.handle_input("Press Enter to continue...")
        encrypt = EncryptionHelper().encrypt_to_bits
        Parser.print_clean("Enter your gender: ")
        gender = Parser.selection_parser(options={"M": "Male", "F": "Female", "N": "Do not disclose"})
        info = encrypt(Parser.string_parser("Enter an intro paragraph about yourself: "))
        notice = encrypt(Parser.string_parser("Enter any allergies or important medical history: "))
        try:
            SQLQuery("INSERT INTO Patient(NHSNo, Gender, Introduction, Notice) VALUES (?, "
                     "?, ?, ?)").commit(parameters=(self.ID, gender, info, notice))
            return True
        except Exception as e:
            print(e)
            print("Database error")
            return False


if __name__ == "__main__":
    current_user = MenuHelper.login()
    MenuHelper.dispatcher(current_user["username"], current_user["user_type"])
    Patient(current_user).main_menu()

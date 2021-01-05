from tabulate import tabulate
from main import User
from encryption import EncryptionHelper
from iohandler import Parser, Paging
from database import SQLQuery
import datetime
from exceptions import DBRecordError
import logging
logger = logging.getLogger("main.Patient")

print_clean = Parser.print_clean
delta = datetime.timedelta
date_now = datetime.datetime.now().date()
dtime_now = datetime.datetime.now()
strptime = datetime.datetime.strptime


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
                options={"B": "book appointments", "I": "view upcoming appointments",
                         "C": "cancel an appointment", "R": "review/rate appointments",
                         "P": "view your prescriptions", "--logout": "Logout"})
            if option_selection == "--logout":
                # Quitting is required for logout to ensure all personal data is cleared from session
                logger.info("User Logged Out")
                print_clean("Logging you out...")
                Parser.user_quit()
            elif option_selection == "B":
                logger.info("Patient booking appointments")
                self.book_appointment_start()
            elif option_selection == "I":
                logger.info("Patient checking in himself")
                self.check_in_appointment()
            elif option_selection == "C":
                logger.info("Patient cancelling appointments")
                self.cancel_appointment()
            elif option_selection == "R":
                r_selection = Parser.selection_parser(options={"A": "review", "B": "rate", "--back": "back"})
                if r_selection == "--back":
                    continue
                elif r_selection == "A":
                    logger.info("Patient reviewing his appointments")
                    self.review_appointment()
                elif r_selection == "B":
                    logger.info("Patient rating his appointments")
                    self.rate_appointment()
            elif option_selection == "P":
                logger.info("Patient reviewing his prescriptions")
                p_selection = Parser.selection_parser(
                    options={"A": "review by input bookingNo", "B": "review by selecting an appointment",
                             "--back": "back"})
                if p_selection == "--back":
                    continue
                elif p_selection == "A":
                    keyword = Parser.string_parser(f"Enter your bookingNo : ")
                    self.review_prescriptions(keyword)
                elif p_selection == "B":
                    self.review_appointment()

    def book_appointment_start(self):
        """
        choose a date -- choose a GP
        --choose time
        --give random number as bookingNo
        --move from available_time
        --insert in visit
        """
        logger.info("Start booking an appointment")
        while True:
            result_table = self.fetch_format_appointments(date_now + delta(days=1), 8)
            print("You are viewing all available appointments for the next week. To view appointments up "
                  "to 2 weeks ahead, use 'select by date' or 'select by GP' options below")
            if not result_table:
                return False

            headers_holder = ["Pointer", "GP Name", "Last Name", "Timeslot"]
            result_index = 4
            Paging.show_page(1, result_table, 5, result_index, headers_holder)

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
    def fetch_format_appointments(selected_date, selected_delta=1, gp_id='%'):
        """
        view the GP's slots that can be booked by patient during selected time scope
        """
        result = SQLQuery("SELECT firstName, lastName, Timeslot, available_time.StaffID FROM "
                          "(available_time JOIN Users ON available_time.StaffID = Users.ID) WHERE "
                          "available_time.StaffID LIKE ? AND Timeslot >= ? AND Timeslot <= ? ORDER BY Timeslot"
                          ).fetch_all(parameters=(gp_id, selected_date, selected_date + delta(days=selected_delta)),
                                      decrypter=EncryptionHelper())
        if len(result) == 0:
            print("There are no available appointments matching the search criteria.")
            logger.info("There are no available appointments matching the search criteria.")
            Parser.handle_input("Press Enter to continue...")
            return False
        result_table = Paging.give_pointer(result)
        return result_table

    def book_appointment_date(self):
        """
        select a timeslot to book appointments
        """
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
            headers_holder = ["Pointer", "GP Name", "Last Name", "Timeslot"]
            result_index = 4
            Paging.show_page(1, result_table, 5, result_index, headers_holder)

            selected_appointment = Parser.list_number_parser("Select an appointment by the Pointer.",
                                                             (1, len(result_table)), allow_multiple=False)
            if selected_appointment == '--back':
                return False
            selected_row = result_table[selected_appointment - 1]
            if self.process_booking(selected_row):
                return True

    def book_appointment_gp(self):
        """
        ---select gp(distinct)
        ---select timeslots for selected gp
        """
        while True:
            gp_result = SQLQuery("SELECT users.firstName, users.lastName, GP.Introduction, GP.ClinicAddress, "
                                 "GP.ClinicPostcode, GP.Gender, GP.Rating, users.ID FROM (GP INNER JOIN users ON "
                                 "GP.ID = users.ID) WHERE users.ID IN ( SELECT DISTINCT StaffID FROM available_time "
                                 "WHERE Timeslot >= ? AND Timeslot <= ? )"
                                 ).fetch_all(parameters=(date_now + delta(days=1), date_now + delta(days=15)),
                                             decrypter=EncryptionHelper())

            gp_table = Paging.give_pointer(gp_result)
            if len(gp_table) == 0:
                print("There are no GPs in the system yet.")
                logger.info("There are no GPs in the system yet.")
                Parser.handle_input("Press Enter to continue...")
                return False

            print(f"You are viewing all available GPs in 2 weeks from: {date_now} ")
            if not gp_table:
                return False

            headers_holder = ["Pointer", "First Name", "Last Name",
                              "Introduction", "Clinic Address",
                              "Clinic Postcode", "Gender", "Rating"]
            result_index = 8
            Paging.show_page(1, gp_table, 5, result_index, headers_holder)

            selected_gp_pointer = Parser.list_number_parser("Select GP by the Pointer.",
                                                            (1, len(gp_table)), allow_multiple=False)
            if selected_gp_pointer == '--back':
                return False
            selected_gp = gp_table[selected_gp_pointer - 1][8]
            result_table = self.fetch_format_appointments(date_now + delta(days=1), 15, selected_gp)
            if not result_table:
                continue
            print(f"You are viewing appointments for the selected GP:")
            logger.info("You are viewing appointments for the selected GP:")
            print(f"You are viewing appointments for the selected GP:")

            headers_holder = ["Pointer", "GP Name", "Last Name", "Timeslot"]
            result_index = 4
            Paging.show_page(1, result_table, 5, result_index, headers_holder)
            selected_appointment = Parser.list_number_parser("Select an appointment by the Pointer.",
                                                             (1, len(result_table)), allow_multiple=False)
            if selected_appointment == '--back':
                return False
            selected_row = result_table[selected_appointment - 1]
            if self.process_booking(selected_row):
                return True

    def process_booking(self, selected_row):
        """
        ---booking appointments
        ---view bookings
        ---edit records(patient info)
        """
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
                    logger.info("Appointment is booked Successfully")
                    visit_result = SQLQuery("SELECT BookingNo, NHSNo, firstName, lastName, Timeslot FROM "
                                            "(Visit JOIN Users ON VISIT.StaffID = Users.ID)"
                                            "WHERE Timeslot = ? AND StaffID = ? "
                                            ).fetch_all(parameters=(selected_row[3], selected_row[4]),
                                                        decrypter=EncryptionHelper())
                    booking_no = visit_result[0][0]
                    logger.info("View your appointments")
                    headers_holder = ["BookingNo", "NHSNo", "GP First Name", "Last Name", "Timeslot"]
                    Paging.better_form(visit_result, headers_holder)
                    Parser.handle_input("Press Enter to continue...")
                except DBRecordError:
                    print("Error encountered")
                    logger.warning("Error in DB")
                    Parser.handle_input("Press Enter to continue...")
                    return False
                info_input = encrypt(Parser.string_parser("Please enter your notes for GP before the visit: "))
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
        while stage == 0:
            appointments = SQLQuery("SELECT bookingNo, NHSNo, firstName, lastName, Timeslot, Confirmed, StaffID FR"
                                    "OM (visit JOIN Users ON visit.StaffID = Users.ID) WHERE NHSNo = ? AND Attended"
                                    " = ? AND Timeslot >= ? "
                                    ).fetch_all(parameters=(self.ID, "F", dtime_now - delta(hours=1)),
                                                decrypter=EncryptionHelper())

            confirmed_appointments = list(appt[0:5] for appt in appointments if appt[5] == "T")
            pending_appointments = list(appt[0:5] for appt in appointments if appt[5] == "P")
            rejected_appointments = list(appt[0:5] for appt in appointments if appt[5] == "F")
            logger.info("You are viewing all your booked appointments: ")
            Parser.print_clean("You are viewing all your booked appointments: ")

            if not appointments:
                print("You have not booked any appointments.")
                logger.info("You have not booked any appointments.")
                Parser.handle_input("Press Enter to continue...")
                return False

            headers_holder = ["Pointer", "BookingNo", "NHSNo", "GP Name", "Last Name", "Timeslot"]

            if confirmed_appointments:
                logger.info("Viewing your confirmed appointments")
                print("Confirmed appointments:")
                Paging.better_form(Paging.give_pointer(confirmed_appointments), headers_holder)

            if pending_appointments:
                logger.info("Viewing your pending appointment")
                print("Pending appointments - wait for confirmation or change appointment:")
                Paging.better_form(Paging.give_pointer(pending_appointments), headers_holder)
            if rejected_appointments:
                logger.info("Viewing your rejected appointments")
                print("Rejected appointments:")
                Paging.better_form(Paging.give_pointer(rejected_appointments), headers_holder)
            print("")
            option_selection = Parser.selection_parser(
                options={"I": "check in confirmed appointment", "C": "change appointment", "--back": "back"})
            if option_selection == "--back":
                return
            elif option_selection == "C":
                return
            elif option_selection == "I":
                stage = 1

        while stage == 1:
            Parser.print_clean("You can only check in within an hour of a scheduled confirmed appointment.")
            check_appt = list(enumerate([appt for appt in appointments if dtime_now - delta(hours=1) <=
                                         strptime(appt[4], '%Y-%m-%d %H:%M:%S') <= dtime_now + delta(hours=1)], 1))
            if not check_appt:
                Parser.handle_input("Press Enter to continue...")
                stage = 0
                continue
            headers_holder = ["Pointer", "BookingNo", "NHSNo", "GP Name", "Last Name", "Timeslot"]
            Paging.better_form(Paging.give_pointer(check_appt), headers_holder)
            logger.info("Select an appointment you want to check in")
            selected_appointment = Parser.list_number_parser("Select an appointment by the Pointer.",
                                                             (1, len(check_appt)), allow_multiple=False)
            if selected_appointment == '--back':
                stage = 0
                continue
            else:
                appointment_check_in = check_appt[selected_appointment - 1][1]
                print("This is the appointment you are checking in for: \n ")
                headers_holder = ["BookingNo", "NHSNo", "GP Name", "Last Name", "Timeslot"]
                Paging.better_form([appointment_check_in[0:5]], headers_holder)

                confirm = Parser.selection_parser(options={"Y": "check-in", "N": "cancel check-in"})
                if confirm == "Y":
                    try:
                        SQLQuery("UPDATE Visit SET Attended = 'T' WHERE BookingNo = ? "
                                 ).commit((appointment_check_in[0],))
                        print("You have been checked in successfully!.")
                        logger.info("Patient check in successfully")
                        Parser.handle_input("Press Enter to continue...")
                        return True
                    except DBRecordError:
                        print("Error encountered")
                        logger.warning("Error in DB")
                        Parser.handle_input("Press Enter to continue...")
                else:
                    print("Removal cancelled.")
                    Parser.handle_input("Press Enter to continue...")
                    stage = 0

    def cancel_appointment(self):
        """
            bookings can be cancelled five days in advance
            move from visit
            insert in available time
            """
        stage = 0
        while stage == 0:
            valid_cancel = SQLQuery("SELECT BookingNo, NHSNo, lastName, Timeslot, PatientInfo, StaffID FROM (visit "
                                    "JOIN Users on visit.StaffID = Users.ID) WHERE NHSNo = ? AND Timeslot >= ?"
                                    ).fetch_all(parameters=(self.ID, dtime_now + delta(days=5)),
                                                decrypter=EncryptionHelper())
            appointments_table = Paging.give_pointer(valid_cancel)
            Parser.print_clean("You are viewing all the appointments can be cancelled.")
            
            if not appointments_table:
                print("There are no Appointments can be cancelled.")
                logger.info("There are no Appointments can be cancelled.")
                print(f"No Appointments can be cancelled.\n")
                return
            else:
                stage = 1

        while stage == 1:
            headers_holder = ["Pointer", "BookingNo", "NHSNo", "GP Name", "Timeslot", "Patient Info"]
            Paging.better_form([appt[0:6] for appt in appointments_table], headers_holder)
            logger.info("Select an appointment you want to cancel")
            selected_cancel_appointment = Parser.list_number_parser("Select an appointment to cancel by the Pointer.",
                                                                    (1, len(appointments_table)), allow_multiple=False)
            selected_row = appointments_table[selected_cancel_appointment - 1]
            Parser.print_clean("This is appointment you want to cancel:")
            Paging.better_form(Paging.give_pointer([selected_row]), headers_holder)
            confirmation = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})

            if confirmation == "Y":
                try:
                    SQLQuery("DELETE FROM visit WHERE BookingNo = ?").commit(parameters=(selected_row[1],))
                    SQLQuery("INSERT INTO available_time VALUES (?,?)").commit(parameters=(selected_row[6],
                                                                                           selected_row[4]))
                    print("Appointment is cancelled successfully.")
                    logger.info("Appointments cancelled successfully")
                except Exception as e:
                    print("Database Error...", e)
                    logger.warning("Error in DB")
            else:
                print("Cancel failed")
                Parser.handle_input("Press Enter to continue...")
                stage = 0

    def review_appointment(self):
        """
        --view unattended appointments
        --view attended appointments
        --choose appointments to view prescription
        --view prescriptions
        """
        stage = 0
        while stage == 0:
            appointments = SQLQuery("SELECT bookingNo, Timeslot, firstName, PatientInfo, Confirmed, Attended, "
                                    "NHSNo, StaffID "
                                    "FROM (visit JOIN Users ON visit.StaffID = Users.ID) WHERE NHSNo = ?"
                                    ).fetch_all(parameters=(self.ID,), decrypter=EncryptionHelper())

            attended_appointments = list(appt[0:5] for appt in appointments if appt[5] == "T")
            unattended_appointments = list(appt[0:5] for appt in appointments if appt[5] == "F")
            Parser.print_clean("You are viewing all your appointments: ")

            if not appointments:
                print("You have no appointments")
                logger.info("You have no appointments.")
                Parser.handle_input("Press Enter to continue...")
                return False

            headers_holder = ["Pointer", "BookingNo", "Timeslot", "GP FirstName", "PatientInfo", "Confirmed"]

            option_selection = Parser.selection_parser(
                options={"A": "View all attended appointments", "U": "view all unattended appointments",
                         "--back": "back"})
            if option_selection == "--back":
                return
            elif option_selection == "U":
                if len(unattended_appointments) == 0:
                    print("You have no unattended bookings")
                    logger.info("You have no unattended bookings.")
                    Parser.handle_input("Press Enter to continue...")
                    return False
                else:
                    logger.info("Viewing your unattended appointments")
                    print("Please do not miss your appointment")
                    Paging.better_form(Paging.give_pointer(unattended_appointments), headers_holder)

            elif option_selection == "A":
                if len(attended_appointments) == 0:
                    print("You have no attended bookings")
                    logger.info("You have no attended bookings.")
                    Parser.handle_input("Press Enter to continue...")
                    return False
                else:
                    stage = 1

        while stage == 1:
            logger.info("Viewing your attended appointments")
            print("attended appointments:")
            Paging.better_form(Paging.give_pointer(attended_appointments), headers_holder)
            selected_appt = Parser.list_number_parser("Select an appointment to view your prescription.",
                                                      (1, len(attended_appointments)), allow_multiple=False)
            selected_row = attended_appointments[selected_appt - 1]
            Parser.print_clean("Choose the appointments you want to see the prescription:")
            Paging.better_form(Paging.give_pointer([selected_row]), headers_holder)
            option_selection = Parser.selection_parser(options={"Y": "view the prescription",
                                                                "N": "Go back and select attended appointments again",
                                                                "--back": "Go back and view all appointments"})
            if option_selection == "--back":
                print("Return and select the type of your appointments again")
                Parser.handle_input("Press Enter to continue...")
                stage = 0

            elif option_selection == "Y":
                try:
                    prescription = SQLQuery("SELECT visit.BookingNo, visit.Diagnosis, prescription.drugName, "
                                            "prescription.quantity, prescription.Instructions "
                                            "FROM visit JOIN prescription ON visit.BookingNo = prescription.BookingNo "
                                            "WHERE visit.BookingNo = ? "
                                            ).fetch_all(parameters=(selected_row[1]), decrypter=EncryptionHelper())
                    Parser.print_clean("You are viewing the prescription: ")

                    if not prescription:
                        print("This appointment do not have prescription")
                        logger.info("No prescription shows.")
                        Parser.handle_input("Press Enter to continue...")
                        return False

                    headers_holder = ["Pointer", "BookingNo", "Diagnosis", "drugName", "quantity", "Instructions"]
                    print("This is your prescription.")
                    Paging.better_form(Paging.give_pointer(prescription), headers_holder)

                except Exception as e:
                    print("Database Error...", e)
                    logger.warning("Error in DB")
            else:
                print("Return and select your appointments again")
                Parser.handle_input("Press Enter to continue...")
                stage = 1

    def rate_appointment(self):
        """
        rate for the attended appointments that has not been attended yet
        """
        stage = 0
        while stage == 0:
            patient_result = SQLQuery("SELECT bookingNo, firstName, lastName, Timeslot, Rating, StaffID FROM (Visit "
                                      "JOIN Users on Visit.StaffID = Users.ID) WHERE NHSNo = ? AND Attended = 'T' "
                                      ).fetch_all(parameters=(self.ID,), decrypter=EncryptionHelper())
            # appointments_table = []
            if not patient_result:
                print("You don't have any attended appointment")
                logger.info("You don't have any attended appointment")
                Parser.handle_input("Press Enter to continue...")
                return False

            # for count, appt in enumerate(patient_result, 1):
            #     appointments_table.append([count, appt[0], appt[1], appt[2], appt[3], appt[4], appt[5]])
            #
            appointments_table = Paging.give_pointer(patient_result)

            Parser.print_clean("These are appointments you have attended:")
            headers = ["Pointer", "BookingNo", "GP Name", "Last Name", "Timeslot"]
            Paging.better_form([appt[0:5] for appt in appointments_table], headers)
            print("Your opinion matters to us. Please take the time to rate your experience with our GP.")
            logger.info("rate your appointment")
            selected_appt = Parser.list_number_parser("Select an appointment to rate by the Pointer.",
                                                      (1, len(appointments_table)), allow_multiple=False)
            if selected_appt == "--back":
                print_clean()
                return False
            selected_appt = int(selected_appt)
            selected_row = appointments_table[selected_appt - 1]
            if not selected_row[5]:
                try:
                    selected_rate = int(
                        Parser.list_number_parser("Select a rating between 1-5. ", (1, 5), allow_multiple=False))
                    current_rate = int(
                        SQLQuery("SELECT Rating FROM GP WHERE ID = ?").fetch_all(parameters=(selected_row[6],))[0][0])
                    rate_count = int(SQLQuery("SELECT COUNT(Rating) FROM Visit WHERE StaffID = ? AND Attended = 'T' "
                                              ).fetch_all(parameters=(selected_row[6],))[0][0])
                    print(current_rate)
                    print(rate_count)
                    if not selected_row[5]:

                        if current_rate != 0:
                            new_rate = round((((current_rate * rate_count) + selected_rate) / (rate_count + 1)), 2)
                        else:
                            new_rate = selected_rate

                        # print(selected_rate)
                        # print(new_rate)
                        SQLQuery("UPDATE Visit SET Rating = ? WHERE BookingNo = ? ").commit(
                            (selected_rate, selected_row[1]))
                        SQLQuery("UPDATE GP SET Rating = ? WHERE ID = ? ").commit((new_rate, selected_row[6]))
                        print("Your rating has been recorded successfully!")
                        logger.info("Your rating has been recorded successfully!")
                        Parser.handle_input("Press Enter to continue...")
                        stage = 0

                except DBRecordError:
                    print("Error encountered")
                    logger.warning("Error in DB")
                    Parser.handle_input("Press Enter to continue...")
            else:

                given_rate = int(SQLQuery("SELECT Rating FROM Visit WHERE BookingNo = ? "
                                          ).fetch_all(parameters=(selected_row[1],))[0][0])
                print(f"Your have rated already! you give {selected_row[2]} {selected_row[3]} a rate of {given_rate}")
                Parser.handle_input("Press Enter to continue...")

    def review_prescriptions(self, selected_bookingno):
        """
        review selected prescriptions
        """
        while True:
            query_string = "SELECT BookingNo, Diagnosis, Notes, PatientInfo " \
                            "FROM visit " \
                            " WHERE BookingNo = ? AND NHSNo = ?"

            headers_holder = ["BookingNo", "Diagnosis", "Notes", "PatientInfo"]
            query = SQLQuery(query_string)
            visit_data = query.fetch_all(decrypter=EncryptionHelper(), parameters=(selected_bookingno, self.ID))

            query_string = "SELECT BookingNo, drugName, quantity, Instructions " \
                           "FROM prescription " \
                           "WHERE BookingNo = ? "
            # headers_holder = ["BookingNo", "Diagnosis", "Notes", "Drug Name", "PatientInfo"]
            query = SQLQuery(query_string)
            prescription_data = query.fetch_all(decrypter=EncryptionHelper(), parameters=(selected_bookingno,))

            if len(list(visit_data)) == 0:
                Parser.print_clean("No such bookingNo.")
                logger.info("No such bookingNo.")
                Parser.handle_input("Press Enter to continue...")
                Parser.print_clean()
                return True
            else:
                print(tabulate(visit_data, headers=headers_holder, tablefmt="fancy_grid", numalign="left"))

                if len(list(prescription_data)) == 0:
                    Parser.print_clean("No Prescriptions Available.")
                    logger.info("No Prescriptions Available.")
                else:
                    print(tabulate([("BookingNo:", prescription_data[0][0]),
                                    ("drugName: ", prescription_data[0][1]),
                                    ("quantity: ", prescription_data[0][2]),
                                    ("Instructions: ", prescription_data[0][3])
                                    ]))

                Parser.handle_input("Press Enter to continue...")
                Parser.print_clean()
                return True

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

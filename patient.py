from tabulate import tabulate
from main import User, MenuHelper
from encryption import EncryptionHelper
from parser_help import Parser
from database_help import SQLQuery
# import sys
import datetime
import random

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
        while True:
            print("You're currently viewing main menu options for Patient {}.".format(self.username))
            option_selection = Parser.selection_parser(
                options={"B": "book appointments", "C": "cancel appiontment", "R": "review appointments",
                         "--logout": "Logout"})
            if option_selection == "--logout":
                # Quitting is required for logout to ensure all personal data is cleared from session
                print_clean("Logging you out...")
                Parser.user_quit()
            elif option_selection == "B":
                self.book_appointment()
            elif option_selection == "C":
                self.cancel_appointment()
            elif option_selection == "R":
                self.review_appointment()


    def book_appointment(self):
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
                selected_date = Parser.date_parser(question=f"Managing for Patient {self.username}.\n"
                                                            "Select a Date:\n")

                if selected_date == "--back":
                    print_clean()
                    return

                # show available GP
                gp_result = SQLQuery(
                    "SELECT DISTINCT StaffID FROM available_time "
                    "WHERE Timeslot >= ? AND Timeslot <= ?",
                ).executeFetchAll(parameters=(selected_date, selected_date + delta(days=1)))
                gp_table = []
                gp_table_raw = []
                gp_pointer = []

                for i in range(len(gp_result)):
                    gp_table.append([i + 1, str(gp_result[i][0])])
                    gp_table_raw.append([i + 1, gp_result[i][0]])
                    gp_pointer.append(i + 1)

                print(f"You are viewing all available GP for: {selected_date}")
                if len(gp_table) == 0:
                    print(f"there is no booking for this day yet.")
                    stage = 0
                    input("Press Enter to continue.")
                else:
                    stage = 1

            while stage == 1:
                # show list of time
                print(tabulate(gp_table, headers=["Pointer", "GP"]))
                selected_gp_pointer = Parser.integer_parser(
                    question="Select entry using number from Pointer column or "
                             "type '--back' to go back")

                print(selected_gp_pointer)

                if selected_gp_pointer not in gp_pointer:
                    print("please choose from this list")
                    stage = 1
                else:
                    #selected_gp = gp_table([selected_gp_pointer],[1])

                    gp_table_raw = gp_table_raw[selected_gp_pointer - 1]
                    # print(selected_gp)
                    appointment_result = SQLQuery(
                        "SELECT StaffID, Timeslot FROM available_time "
                        "WHERE StaffID = ? AND Timeslot >= ? AND Timeslot <= ?",
                    ).executeFetchAll(parameters=(gp_table_raw[1], selected_date, selected_date + delta(days=1)))


                    appointment_table = []
                    appointment_table_raw = []
                    appointment_pointer = []

                    for i in range(len(appointment_result)):
                        appointment_table.append([i + 1, str(appointment_result[i][0]), str(appointment_result[i][1])])
                        appointment_table_raw.append([i + 1, appointment_result[i][0], appointment_result[i][1]])
                        appointment_pointer.append(i + 1)
                    print(f"You are viewing your schedule for: {selected_date}")

                    if len(appointment_table) == 0:
                        print(f"there is no booking for this day yet.")
                        input("Press Enter to continue...")
                        stage = 0
                    else:
                        print(tabulate(appointment_table, headers=["Pointer", "GP", "Timeslot"]))

                        stage = 2

            while stage == 2:
                selected_appointment = Parser.integer_parser(question="Select entry using number from Pointer column or "
                                                            "type '--back' to go back")
                if selected_appointment == '--back':
                    return False


                if selected_appointment not in appointment_pointer:
                    print("please choose from this list")
                    stage = 2
                else:

                    selected_row = appointment_table[selected_appointment - 1]
                    selected_row_raw = appointment_table_raw[selected_appointment - 1]

                    print("This is time slot will be booked by you:")

                    print(tabulate([selected_row], headers=["Pointer", "GP", "Timeslot"]))

                    confirm = Parser.selection_parser(options={"Y": "Confirm", "N": "Go back and select again"})
                    # Confirm if user wants to delete slots
                    if confirm == "Y":
                        try:
                            repeat_booking_num = 1
                            while (repeat_booking_num ):
                                booking_no = random.randint(100000, 999999)
                                #bookingNum = random.randint(1, 3)
                                #bookingNum = 1
                                visit_same_booking_no = SQLQuery("SELECT bookingNo FROM visit WHERE bookingNo = ? ").executeFetchAll(parameters=(booking_no,))
                                if len(visit_same_booking_no) == 0:
                                    #repeat_booking_num = 0
                                    break
                                else:
                                    repeat_booking_num  = 1

                            visit_same_booking_num = SQLQuery(
                                "SELECT Timeslot FROM visit WHERE Timeslot = ? ").executeFetchAll(parameters=(selected_row_raw[2],))
                            if len(visit_same_booking_no) != 0:
                                # repeat_timeslot_num = 0
                                print("This time slot has been booked")
                                return False
                            else:

                                SQLQuery("INSERT INTO visit VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                                         ).executeCommit((booking_no,self.ID,selected_row_raw[1],selected_row_raw[2],"","F","F","","","0"))
                                SQLQuery("DELETE FROM available_time WHERE StaffID = ? AND Timeslot = ?"
                                         ).executeCommit((selected_row_raw[1], selected_row_raw[2]))

                                print("booked successfully.")

                                visit_result = SQLQuery("SELECT bookingNo, NHSNo, StaffID, Timeslot FROM visit "
                                                        "WHERE bookingNo = ? "
                                                        ).executeFetchAll(parameters=(booking_no,))

                                print(tabulate(visit_result, headers=["bookingNo","NHSNo", "GP", "Timeslot"]))

                                stage = 3

                                input("Press Enter to continue...")

                        except:
                            print("Error encountered")
                            input("Press Enter to continue...")
                    if confirm == "N":
                        print("book cancelled.")
                        slots_to_remove = []
                        input("Press Enter to continue...")

                while stage == 3:
                    print_clean("")

                    info_input = Parser.string_parser("Please write description about your illness before the appointment: ")
                    SQLQuery(" UPDATE Visit SET PatientInfo = ? WHERE BookingNo = ? "
                             ).executeCommit((info_input,booking_no))
                    Parser.print_clean("Your description have been recorded successfully!")
                    Parser.string_parser("Press Enter to continue...")
                    return True




    def cancel_appointment(self):
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
                               "visit.PatientInfo, visit.Diagnosis, visit.Notes, prescription.drugName, " \
                               "prescription.quantity, prescription.Instructions " \
                               "FROM (visit INNER JOIN users ON visit.NHSNo = users.ID) " \
                               "INNER JOIN prescription ON " \
                               "visit.BookingNo = prescription.BookingNo WHERE visit.NHSNo = ? "

                headers = ("BookingNo", "NHSNo", "Firstname", "Lastname", "PatientInfo", "Diagnosis",
                           "DrugName", "Quantity", "Instructions", "Notes")

            query = SQLQuery(query_string)
            all_data = query.executeFetchAll(decrypter=EncryptionHelper(), parameters=(self.ID,))

            if len(list(all_data)) == 0:
                Parser.print_clean("No records Available.\n")
            else:
                print(tabulate(all_data, headers))


if __name__ == "__main__":
    current_user = MenuHelper.login()
    MenuHelper.dispatcher(current_user["username"], current_user["user_type"])
    Patient(current_user).main_menu()

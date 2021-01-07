import time
import datetime
import sys
from typing import Iterable, Union
from exceptions import *
from tabulate import tabulate
import os


class Parser:
    """
    Helper class for collecting and validating user inputs in a command-line interface.
    """

    @staticmethod
    def integer_parser(question, allow_back=True) -> Union[str, int]:
        """
        Method to collect valid integer input from user.

        :param str question: Prompt for the user
        :param bool allow_back: Specific whether '--back' is an allowed input
        """
        while True:
            try:
                print(question)
                input_string = Parser.handle_input(input_question="")
                if allow_back and input_string == '--back':
                    return input_string
                else:
                    result = int(input_string)
                    return result
            except (ValueError, TypeError) as e:
                Parser.print_clean("This is not a valid integer !", e)

    @staticmethod
    def time_parser(question, limit_quarter_intervals=True, allow_back=True) -> datetime:
        """
        Method to collect valid time input from user.

        :param str question: Prompt for the user
        :param bool limit_quarter_intervals: If true, only 0, 15, 30, 45 are valid minutes
        :param bool allow_back: Specific whether '--back' is an allowed input
        """

        while True:
            try:
                Parser.print_clean(question + " Please input datetime in this format 'HH:MM'")
                if allow_back:
                    print("Or enter '--back' to go back to previous page")
                user_input = Parser.handle_input(input_question="")
                if allow_back and user_input == '--back':
                    return user_input
                input_time = datetime.datetime.strptime(user_input, '%H:%M').time()
                if datetime.time(8, 30, 0) > input_time or input_time > datetime.time(19, 0, 0):
                    raise ValueError
                elif not limit_quarter_intervals:
                    return input_time
                else:
                    if input_time.minute in [0, 15, 30, 45]:
                        return input_time
                    else:
                        raise NotQuarterIntervalError
            except ValueError:
                print("This is not a valid time, or it is outside of the allowed working hours: 8:30 - "
                      "19:00!")
                Parser.handle_input("Press Enter to continue...")
            except NotQuarterIntervalError:
                print("Appointments are limited to 15 min sessions!")
                Parser.handle_input("Press Enter to continue...")

    @staticmethod
    def date_parser(question, allow_back=True, allow_past=False) -> datetime:
        """
        Method to collect valid date input from user.

        :param bool allow_past: Specify whether a date in the past is allowed
        :param str question: Prompt for the user
        :param bool allow_back: Specific whether '--back' is an allowed input
        """
        while True:
            try:
                Parser.print_clean(question + " Please input date in the following format 'YYYY-MM-DD'")
                if allow_back:
                    print("Or enter '--back' to go back to previous page")
                user_input = Parser.handle_input(input_question="")
                if allow_back and user_input == '--back':
                    return user_input
                else:
                    date = datetime.datetime.strptime(user_input, '%Y-%m-%d').date()
                    if not allow_past:
                        if date < datetime.datetime.now().date() or \
                                date > datetime.datetime.now().date() + datetime.timedelta(days=182):
                            raise ValueError
                    else:
                        if date > datetime.datetime.now().date():
                            raise ValueError
                    return date
            except ValueError:
                print("This is not a valid date! Either the format is incorrect, it is earlier than "
                      "today, or it is more than 6 months ahead.")
                Parser.handle_input("Press Enter to continue...")

    @staticmethod
    def nhs_no_parser(question="Please input your NHS Number") -> int:
        """
        Method to collect a valid NHS number from user.

        :param str question: Prompt for the user
        """
        while True:
            try:
                print(question)
                result = int(Parser.handle_input(input_question=""))
                if 1000000000 <= result <= 9999999999:
                    return result
                else:
                    raise ValueError
            except (ValueError, TypeError) as e:
                Parser.print_clean("This is not a valid NHS Number!", e)

    @staticmethod
    def admin_no_parser(question="Please input admin Staff Number") -> str:
        """
        Method to collect a valid admin Staff Number from user.

        :param str question: Prompt for the user
        """
        while True:
            try:
                print(question)
                result = Parser.handle_input(input_question="")
                # testing if the rest of the string is integer
                int(result[1:10])
                if result[0] != 'A' or len(result) != 10:
                    raise ValueError
                return result
            except (ValueError, TypeError) as e:
                Parser.print_clean("Invalid Admin number, format required: A#########!", e)

    @staticmethod
    def gp_no_parser(question="Please input GP Staff Number") -> str:
        """
        Method to collect a valid admin Staff Number from user.

        :param str question: Prompt for the user
        """
        while True:
            try:
                print(question)
                result = Parser.handle_input(input_question="")
                # testing if the rest of the string is integer
                int(result[1:10])
                if result[0] != 'G' or len(result) != 10:
                    raise ValueError
                return result
            except (ValueError, TypeError) as e:
                print("Invalid GP number, format required: G#########!", e)

    @staticmethod
    def selection_parser(options={"--back": "back"}) -> str:
        """
        Method to collect a valid selection from the user.

        :rtype: object
        :param dict options: Dictionary of the allowed options
        """
        while True:
            try:
                print("Please select from the following options:")
                if "--back" in options.keys():
                    del options["--back"]
                    options["--BACK"] = "back"
                elif "--logout" in options.keys():
                    del options["--logout"]
                    options["--LOGOUT"] = "logout"

                for key in options:
                    print(f"Enter '{key}' to {options[key]}")

                result = Parser.handle_input(input_question="").strip().upper()

                if result == "--QUIT":
                    Parser.user_quit()
                if result not in options:
                    raise ValueError
                if any(result == option for option in ["--BACK", "--LOGOUT"]):
                    result = result.lower()
                return result
            except ValueError:
                Parser.print_clean("Invalid Input!\n")

    @staticmethod
    def list_number_parser(question, full_num_range, allow_back=True, allow_multiple=True) -> Union[list, str]:
        """
        Method to collect and process a range selection from user

        :param str question: Prompt for the user
        :param bool allow_multiple: True allows user to input a selection like 1-5, 6-10 etc.
        :param tuple full_num_range: (a, b)-like tuple specifying upper and lower bounds of the range
        :param bool allow_back: Specific whether '--back' is an allowed input
        """
        while True:
            try:
                print(question)
                if allow_multiple:
                    print("Use ',' to separate values.")
                    print("Use 'a-b' to select the number in range a to b inclusive")
                    if allow_back:
                        print("Or enter '--back' to go back to previous page")
                    result_final = []
                    result_raw = Parser.handle_input(input_question="")
                    if allow_back and result_raw == '--back':
                        return result_raw
                    result_raw = (result_raw.strip(" ")).split(',')
                    for element in result_raw:
                        if '-' not in element:
                            result_final.append(int(element))
                        else:
                            num_range = element.split('-')
                            # map is a generator!!!
                            num_range = list(map(int, num_range))
                            list_num_range = list(range(min(num_range), max(num_range) + 1))
                            result_final += list_num_range
                    result_final = list(set(result_final))
                    for num in result_final:
                        if not min(full_num_range) <= num <= max(full_num_range):
                            raise ValueError
                    result_final.sort()
                    return result_final
                else:
                    if allow_back:
                        print("Or enter '--back' to go back to previous page")
                        input_string = Parser.handle_input(input_question="")
                    if allow_back and input_string == '--back':
                        return input_string
                    else:
                        result = int(input_string)
                        if not min(full_num_range) <= result <= max(full_num_range):
                            raise ValueError
                        return result
            except ValueError:
                Parser.print_clean("Invalid input! Either not an integer or out of range.")

    @staticmethod
    def user_quit() -> None:
        """Method to quit the application on request."""
        print("Application quitting...")
        time.sleep(3)
        sys.exit(1)

    @staticmethod
    def print_clean(*args) -> None:
        """
        Method which can be used to print message(-s) after cleaning the terminal window.

        :param str args: Messages to be printed
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        for message in args:
            print(message)

    @staticmethod
    def string_parser(question) -> str:
        """
        Method to collect string input from user.

        :param str question: Prompt for the user
        """
        while True:
            try:
                Parser.print_clean(question)
                result = Parser.handle_input(input_question="")
                if result == "--quit":
                    Parser.user_quit()
                elif result == "":
                    continue
                else:
                    return result
            except ValueError:
                print("Invalid Input")

    @staticmethod
    def handle_input(input_question="Press Enter to Continue: "):
        """
        Method to handle keyboard interrupt exception on user input.

        :param str input_question: Prompt for the user
        """
        while True:
            try:
                return input(input_question)
            except KeyboardInterrupt:
                continue


class Paging:
    """
    Help with print and pointer
    """

    @staticmethod
    def show_page(page, all_data_table, step, index, headers_holder):
        """
        Method to show data in pages, must choose C to leave pages

        :param int page: page index
        :param list all_data_table: lists of data list, all data before divided into pages, can be result of SQL.
        :param int step: the number of data lists will show in a page
        :param int index: help to use only part of data in one list, order matters
                          for example,data in one list like [1,name, timeslot, StaffID], index = 3 to hide StaffID 
        :param list headers_holder: a list of table columns' name

        """
        if step == 0:
            print("step must > 0")
        else:
            end = len(all_data_table)/step + 1 if len(all_data_table) % step != 0 else len(all_data_table)/step
            start = 0 + (page-1)*step
            stop = start + step
            current = []
            for row in all_data_table[start: stop]:
                current.append(row[0:index])

            print(tabulate(current, headers=headers_holder,
                           tablefmt="fancy_grid",
                           numalign="left"))
            print("Page: - " + str(page) + " - ")

            user_input = Parser.selection_parser(
                options={"A": " <-- back to previous page ", "D": " --> Proceed to next page ",
                         "C": "Continue to next part"})
            if user_input == "D":
                page += 1
                if page > end:
                    print("already the last page")
                    input("Press Enter to Continue...")
                    Paging.show_page(page - 1, all_data_table, step, index, headers_holder)
                else:
                    Paging.show_page(page, all_data_table, step, index, headers_holder)
            elif user_input == "A":
                page -= 1
                if page == 0:
                    print("already the first page")
                    input("Press Enter to Continue...")
                    Paging.show_page(page + 1, all_data_table, step, index, headers_holder)
                else:
                    Paging.show_page(page, all_data_table, step, index, headers_holder)
            else:
                return

    @staticmethod
    def give_pointer(result):
        """
        Method to add pointer for each line.

        :param list result: list to add pointer

        """
        result_table = []
        for count, item in enumerate(result):
            table_list = [count + 1]
            if not isinstance(item, Iterable) or isinstance(item, str):
                table_list.append(item)
            else:
                table_list.extend(item)
            result_table.append(table_list)
        return result_table

    @staticmethod
    def better_form(data, headers_holder):
        """
        Method to print table.

        :param list data: data to print
        :param list headers_holder: a list of table columns' name
        """
        print(tabulate(data, headers=headers_holder, tablefmt="fancy_grid", numalign="left"))
        return

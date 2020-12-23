from datetime import datetime, timedelta, time
import sys
from typing import Union

from exceptions import *
import os


# noinspection PyUnusedLocal
class Parser:
    """
    Helper class for collecting and validating user inputs in a command-line interface.
    """

    @staticmethod
    def integer_parser(question, allowback=True) -> Union[str, int]:
        """
        Method to collect valid integer input from user.

        :param str question: Prompt for the user
        :param bool allowback: Specific whether '--back' is an allowed input
        """
        while True:
            try:
                print(question)
                input_string = input()
                if allowback and input_string == '--back':
                    return input_string
                else:
                    result = int(input_string)
                    return result
            except (ValueError, TypeError) as e:
                Parser.print_clean("This is not a valid integer !")

    @staticmethod
    def time_parser(question, limit_quarter_intervals=True, allowback=True) -> object:
        """
        Method to collect valid time input from user.

        :param str question: Prompt for the user
        :param bool limit_quarter_intervals: If true, only 0, 15, 30, 45 are valid minutes
        :param bool allowback: Specific whether '--back' is an allowed input
        """

        while True:
            try:
                Parser.print_clean(question + " Please input datetime in this format 'HH:MM'")
                if allowback:
                    print("Or enter '--back' to go back to previous page")
                user_input = input()
                if allowback and user_input == '--back':
                    return user_input
                input_time = datetime.strptime(user_input, '%H:%M').time()
                if time(8, 30, 0) > input_time or input_time > time(19, 0, 0):
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
                input("Press Enter to continue...")
            except NotQuarterIntervalError:
                print("Appointments are limited to 15 min sessions!")
                input("Press Enter to continue...")

    @staticmethod
    def date_parser(question, allowback=True) -> object:
        """
        Method to collect valid date input from user.

        :param str question: Prompt for the user
        :param bool allowback: Specific whether '--back' is an allowed input
        """
        while True:
            try:
                Parser.print_clean(question + " Please input date in the following format 'YYYY-MM-DD'")
                if allowback:
                    print("Or enter '--back' to go back to previous page")
                user_input = input()
                if allowback and user_input == '--back':
                    return user_input
                else:
                    date = datetime.strptime(user_input, '%Y-%m-%d').date()
                    if date < datetime.now().date() or date > datetime.now().date() + timedelta(days=182):
                        raise ValueError
                    return date
            except ValueError:
                print("This is not a valid date! Either the format is incorrect, it is earlier than "
                      "today, or it is more than 6 months ahead.")
                input("Press Enter to continue...")

    @staticmethod
    def nhs_no_parser(question="Please input your NHS Number") -> int:
        """
        Method to collect a valid NHS number from user.

        :param str question: Prompt for the user
        """
        while True:
            try:
                print(question)
                result = int(input())
                if 1000000000 <= result <= 9999999999:
                    return result
                else:
                    raise ValueError
            except (ValueError, TypeError) as e:
                Parser.print_clean("This is not a valid NHS Number!")

    @staticmethod
    def admin_no_parser(question="Please input admin Staff Number") -> str:
        """
        Method to collect a valid admin Staff Number from user.

        :param str question: Prompt for the user
        """
        while True:
            try:
                print(question)
                result = input()
                # testing if th rest o the string is integer
                int(result[1:10])
                if result[0] != 'A' or len(result) != 10:
                    raise ValueError
                return result
            except (ValueError, TypeError) as e:
                Parser.print_clean("Invalid Admin number, format required: A########!")

    @staticmethod
    def gp_no_parser(question="Please input GP Staff Number") -> str:
        """
        Method to collect a valid admin Staff Number from user.

        :param str question: Prompt for the user
        """
        while True:
            try:
                print(question)
                result = input()
                # testing if th rest o the string is integer
                int(result[1:10])
                if result[0] != 'G' or len(result) != 10:
                    raise ValueError
                return result
            except (ValueError, TypeError) as e:
                print("Invalid GP number, format required: G########!")

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
                for key in options:
                    print(f"Enter '{key}' to {options[key]}")
                result = input()
                if result == "--quit":
                    Parser.user_quit()
                if result not in options:
                    raise ValueError
                return result
            except ValueError:
                Parser.print_clean("Invalid Input!")

    @staticmethod
    def list_number_parser(question, full_num_range, allowback=True) -> Union[list, str]:
        """
        Method to collect and process a range selection from user

        :param str question: Prompt for the user
        :param tuple full_num_range: (a, b)-like tuple specifying upper and lower bounds of the range
        :param bool allowback: Specific whether '--back' is an allowed input
        """
        while True:
            try:
                print(question)
                print("Use ',' to separate values.")
                print("Use 'a-b' to select the number in range a to b inclusive")
                if allowback:
                    print("Or enter '--back' to go back to previous page")
                result_final = []
                result_raw = input()
                if allowback and result_raw == '--back':
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
                        # print(listNumRange)
                        result_final += list_num_range
                result_final = list(set(result_final))
                # print(resultFinal)
                for num in result_final:
                    if not min(full_num_range) <= num <= max(full_num_range):
                        raise ValueError
                result_final.sort()
                return result_final
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
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
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
                result = input()
                if result == "--quit":
                    Parser.user_quit()
                else:
                    return result
            except ValueError:
                print("Invalid Input")

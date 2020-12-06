import datetime
from databaseHelp import database
import time

class not0Or30Min(Exception):
    '''
    error class created for datetime object
    '''
    pass

class DBRecordError(Exception):
    '''
    error class created for datetime object
    '''
    pass



class parser:
    @staticmethod
    def stringParser(question):
        """
        looping function until a valid answer is inputted
        :prara question: qustion to ask user
        :return: the string answer
        """
        while True:
            try:
                print(question)
                result = input()
                return result
            except:
                print("Invalid Input")
    
    @staticmethod
    def integerParser(question):
        """
        repeat until a valid integer is inputted
        :param question: qustion to ask user
        :return: the integer answer
        """
        while True:
            try:
                print(question)
                result = int(input())
                return result
            except ValueError:
                print("This is not a valid integer")
    @staticmethod
    def datetimeParser(question, limitToHalfHourInterval=False):
        """
        repeat until a valid datetime is inputted
        :param question: qustion to ask user
        :param limitToHalfHourInterval: if set to true it only time with 00 Min or 30 Min will be valid
        :return: the datetime answer
        """
        while True:
            try:
                print(question, "Please input datetime in this format 'YYYY-MM-DD HH:MM'")
                inputString = input()
                inputDatetime = datetime.datetime.strptime(inputString, '%Y-%m-%d %H:%M')
                if limitToHalfHourInterval==False :
                    return inputDatetime
                else:
                    if inputDatetime.minute == 0 or inputDatetime.minute == 30:
                        return inputDatetime
                    else:
                        raise not0Or30Min()
            except ValueError:
                print("This is not a valid date and time")

            except not0Or30Min:
                print("Appiontments are limited to half hour session")    

    @staticmethod
    def dateParser(question):
        """
        repeat until a valid datet is inputted
        :param question: qustion to ask user
        :return: the datetime answer
        """
        while True:
            try:
                print(question, "Please input datetime in this format 'YYYY-MM-DD'")
                inputString = input()
                inputDate = datetime.datetime.strptime(inputString, '%Y-%m-%d')
                return inputDate
            except ValueError:
                print("This is not a valid date")

    @staticmethod
    def nhsNoParser(question="Please Input your NHS Number"):
        """
        repeat until a valid NHS No is inputted
        :param question: qustion to ask user
        :return: the nhsNo answer
        """
        while True:
            try:
                print(question)
                result = int(input())
                if 1000000000 <= result <= 9999999999:
                    return result
                else:
                    raise ValueError
            except ValueError:
                print("This is not a valid NHSNo")

    @staticmethod
    def AdminStaffNoParser(question="Please Input Admin's Staff Number"):
        """
        repeat until a valid Admin Staff No is inputted
        :param question: qustion to ask user
        :return: the Admin Staff No answer
        """
        while True:
            try:
                print(question)
                result = input()
                #testing if th rest o the string is integer
                int(result[1:10])
                if result[0] != 'A' or len(result) != 10:
                    raise ValueError
                return result
            except ValueError:
                print("Invalid number for Admin Staff, Format should be A########")   
    @staticmethod
    def GPStaffNoParser(question="Please Input GP's Staff Number"):
        """
        repeat until a valid GP Staff No is inputted
        :param question: qustion to ask user
        :return: the GP Staff No answer
        """
        while True:
            try:
                print(question)
                result = input()
                #testing if th rest o the string is integer
                int(result[1:10])
                if result[0] != 'G' or len(result) != 10:
                    raise ValueError
                return result
            except ValueError:
                print("Invalid number for Admin Staff, Format should be G########")   

    @staticmethod
    def TrueFalseParser(question):
        """
        looping function until a valid true or false is inputted
        :prara question: qustion to ask user
        :return: the character answer
        """
        while True:
            try:
                print(question)
                result = input()
                result = result.upper()
                if result not in ['T', 'F']:
                    raise ValueError
                return result
            except ValueError:
                print("only 'T' (for true) or 'F' (for false) are allowed")

    @staticmethod
    def TrueFalsePendingParser(question):
        """
        looping function until a valid Pending true or false is inputted
        :prara question: qustion to ask user
        :return: the character answer
        """
        while True:
            try:
                print(question)
                result = input()
                result = result.upper()
                if result not in ['P', 'T', 'F']:
                    raise ValueError
                return result
            except ValueError:
                print("only 'P' (for pending), 'T' (for true) or 'F' (for false) are allowed")

    def RegisterOrLoginParser():
        """
        looping function until a valid true or false is inputted
        :prara question: qustion to ask user
        :return: the character answer
        """
        while True:
            try:
                print("Do you want to Login or Register as new user")
                print("Enter 'L' to Login")
                print("Enter 'R' to Register")
                result = input()
                result = result.upper()
                if result not in ['L', 'R']:
                    raise ValueError
                return result
            except ValueError:
                print("only 'L' (for Login) or 'R' (for Register) are allowed")


if __name__ == "__main__":
    # print(parser.integerParser("type in Integer"))
    # print(parser.datetimeParser("type in datetime no limit"))
    # print(parser.datetimeParser("type in datetime no limit", limitToHalfHourInterval=True))
    # print(parser.dateParser("Date question"))
    # print(parser.AdminStaffNoParser())
    # print(parser.nhsNoParser())
    # print(parser.GPStaffNoParser())
    # print(parser.TrueFalsePendingParser("tfp"))
    # print(parser.TrueFalseParser('tf'))
    pass

import datetime
from databaseHelp import database
import time
import os


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
            except ValueError:
                print("Invalid Input")
    
    @staticmethod
    def integerParser(question, allowback=True):
        """
        repeat until a valid integer is inputted
        :param question: qustion to ask user
        :return: the integer answer
        """
        while True:
            try:
                print(question)
                inputString = input()
                if (allowback == True) and (inputString == '--back'):
                    return inputString
                else:
                    result = int(inputString)
                    return result
            except ValueError:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("This is not a valid integer !")
    @staticmethod
    def timeParser(question, limitToHalfHourInterval=True, allowback=True):
        """
        repeat until a valid datetime is inputted
        :param question: qustion to ask user
        :param limitToHalfHourInterval: if set to true it only time with 00 Min or 30 Min will be valid
        :return: the datetime answer
        """
        while True:
            try:
                print(question, "Please input datetime in this format 'HH:MM'")
                if allowback == True:
                    print("Or enter '--back' to go back to previous page")
                inputString = input()
                if allowback == True and inputString == '--back':
                    return inputString
                inputDatetime = datetime.datetime.strptime(inputString, '%H:%M')
                if limitToHalfHourInterval==False :
                    return inputDatetime
                else:
                    if inputDatetime.minute in [0, 15, 30, 45]:
                        return inputDatetime
                    else:
                        raise not0Or30Min()
            except ValueError:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("This is not a valid date and time!")

            except not0Or30Min:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Appiontments are limited to 15 min session!")    

    @staticmethod
    def dateParser(question, allowback=True):
        """
        repeat until a valid datet is inputted
        :param question: qustion to ask user
        :return: the datetime answer
        """
        while True:
            try:
                print(question, "Please input datetime in this format 'YYYY-MM-DD'")
                if allowback == True:
                    print("Or enter '--back' to go back to previous page")
                inputString = input()
                if allowback == True and inputString == '--back':
                    return inputString
                inputDate = datetime.datetime.strptime(inputString, '%Y-%m-%d')
                return inputDate
            except ValueError:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("This is not a valid date!")

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
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("This is not a valid NHSNo!")

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
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Invalid number for Admin Staff, Format should be A######## !")   
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
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Invalid number for Admin Staff, Format should be G######## !")   

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
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("only 'T' (for true) or 'F' (for false) are allowed !")

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
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("only 'P' (for pending), 'T' (for true) or 'F' (for false) are allowed !")

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
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("only 'L' (for Login) or 'R' (for Register) are allowed")

    def selectionParser(options={"--back": "back"}):
        """
        prompt to ask for valid input from a user
        :param options: dictionary to store valid response
        :return: input
        """
        while True:
            try:
                print("Please select the following options:")
                for key in options:
                    print(f"Enter '{key}' to {options[key]}")
                
                result = input()
                if result not in options:
                    raise ValueError
                return result
            except ValueError:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Invalid Input!!")
    def listNumberParser(question, fullNumRange, allowback=True):
        """
        prompt to ask for number range from a user
        :param options: dictionary to store valid response
        :return: list of unique integer selected by user
        """
        while True:
            try:
                print(question)
                print("use ',' to separate each value")
                print("use 'a-b' to select the number in range a to b inclusive")
                if allowback == True:
                    print("Or enter '--back' to go back to previous page")
                resultFinal = []
                resultRaw = input()
                if allowback == True and resultRaw == '--back':
                    return resultRaw
                resultRaw = resultRaw.replace(" ", "")    
                resultList = resultRaw.split(',')
                for element in resultList:
                    if '-' not in element:
                        resultFinal.append(int(element))
                    else:
                        numRange = element.split('-')
                        #map is a generator!!!
                        numRange = list(map(int,numRange))
                        #print(numRange)
                        listNumRange = list(range(min(numRange), max(numRange)+1))
                        #print(listNumRange)
                        resultFinal += listNumRange
                resultFinal = list(set(resultFinal))
                #print(resultFinal)
                for num in resultFinal:
                    if not min(fullNumRange) <= num <= max(fullNumRange):
                        raise ValueError
                resultFinal.sort()
                return resultFinal
            except ValueError:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Invalid Input!! either not an integer or out of range")

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
    # print(parser.selectionParser(options={"A": "add availability","C": "confirm bookings","S": "start appointment","--back": "back to previous page"}))
    # print(parser.listNumberParser("numrange test", (2,15)))
    pass

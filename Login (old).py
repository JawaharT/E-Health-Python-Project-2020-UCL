from database import SQLQuery
from parser_help import Parser
from encryption import EncryptionHelper
from encryption import PasswordHelper
import time
import sys
import getpass
import os


class DBRecordError(Exception):
    '''
    error class created for datetime object
    '''
    pass


class notMatchError(Exception):
    '''
    error class created for datetime object
    '''
    pass


class userInterruption(Exception):
    '''
    error class for user interruption
    '''
    pass


class currentUser():
    def __init__(self, username, encryptionKey):
        '''
        return a currentUser Object to remember the information of current user.
        '''
        self.username = username
        self.encryptionKey = encryptionKey
        # retrieving the full information from DATAbase instead of just the password for authentication
        fullUQuerry = SQLQuery(
            "SELECT ID, passCode, firstName, lastName, phoneNo, HomeAddress, postCode, birthday, UserType FROM Users WHERE username == ?")
        fullUserArray = fullUQuerry.executeFetchAll(decrypter=self.encryptionKey, parameters=(self.username,))
        # loading the user info into a state
        self.ID = fullUserArray[0][0]
        self.passCode = fullUserArray[0][1]
        self.firstName = fullUserArray[0][2]
        self.lastName = fullUserArray[0][3]
        self.phoneNo = fullUserArray[0][4]
        self.HomeAddress = fullUserArray[0][5]
        self.postCode = fullUserArray[0][6]
        self.birthday = fullUserArray[0][7]
        self.UserType = fullUserArray[0][8]


class loginHelp():
    def Login():
        """
        :return: False: for failed or calceled login; tuple(username, encryption key for database) if login successful
        prompt the user for information and check if the username, password are correct and account is no deactivated.
        if successful, it will load the encrypion Key and return the username for the current user session object construction.
        """
        while True:
            stage = 0
            loginUsername = None
            if stage == 0:
                loginUsername = loginHelp.checkUserName()
                # print(loginUsername)
                if loginUsername == False:
                    return False
                else:
                    stage = 1
            if stage == 1:
                checkPW = loginHelp.checkPW(loginUsername)
                print(checkPW)
                # print(checkPW)
                if checkPW == True:
                    stage = 2
                else:
                    stage = 0
            if stage == 2:
                checkDeactivated = loginHelp.checkDeactivated(loginUsername)
                if checkDeactivated == False:
                    # return the username and loading the encryption key for use
                    print("not Deactivated")
                    key = encryptionHelper()
                    return (loginUsername, key)

    @staticmethod
    def checkUserName():
        """
        :return: False for incorrect username or calceled login; str(username) if user exist
        prompt the user to enter the username and check against the DB.
        """
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        while True:
            # trying to get username
            tryUsername = parser.stringParser("Please enter your username OR '--back' to go back")
            # retrieving the user if exist to compare to PW
            usernameQuerry = SQLQuerry("SELECT username FROM Users WHERE username == ?")
            qResult = usernameQuerry.executeFetchAll(parameters=(tryUsername,))
            if tryUsername == '--back':
                return False
            if len(qResult) == 1 and qResult[0][0] == tryUsername:
                print("username correct")
                return tryUsername
            else:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Incorrect UserName!!!")

    @staticmethod
    def checkPW(username):
        """
        :param (username): username to check the password
        :return: (bool) False for calceled password enter; true if password is correct.
        prompt the user to enter the username and check against the DB.
        """
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        for i in range(4, -1, -1):
            try:
                # the PW is saved in hash so need to convert to hash to compare special parsing function becasue it will hide the needed
                PWQuerry = SQLQuerry("SELECT passCode FROM Users WHERE username == ?")
                qResult = PWQuerry.executeFetchAll(parameters=(username,))
                tryPW = passwordHelper.hashPW(getpass.getpass("Enter your password: "))
                if tryPW == '--back':
                    return False
                if tryPW == qResult[0][0]:
                    # load encryption key if PW is correct
                    print("Password Correct")
                    return True
                else:
                    raise DBRecordError
            except DBRecordError:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print(f"Invalid Password {i} attempts remaining")
        else:
            print("Too many wrong PW attempt. terminating ...")
            time.sleep(3)
            sys.exit(1)

    @staticmethod
    def checkDeactivated(username):
        """
        :param (username): username to check the password
        :return: (bool) False for deactivated user
        check against the DB to see if the user is deactivated.
        """
        DAQuerry = SQLQuerry("SELECT Deactivated FROM Users WHERE username == ?")
        qResult = DAQuerry.executeFetchAll(parameters=(username,))
        if qResult[0][0] == "F":
            return False
        else:
            print("Your account is deactvated, terminating ...")
            time.sleep(3)
            sys.exit(1)


if __name__ == "__main__":
    # tryQuerry = SQLQuerry("SELECT ID, username, passCode, firstName, lastName, phoneNo, HomeAddress, postCode, UserType, deactivated  FROM Users WHERE username == ?")
    # EH = encryptionHelper()
    # result = tryQuerry.executeFetchAll(decrypter=EH, parameters=('testGP',))
    # print(result)
    # print(user.ID, user.username, user.passCode, user.firstName, user.lastName, user.phoneNo, user.HomeAddress, user.postCode, user.UserType, user.deactivated)
    pas
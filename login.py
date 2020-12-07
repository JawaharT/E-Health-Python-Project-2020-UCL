from databaseHelp import SQLQuerry
from parserHelp import parser
from encryption import encryptionHelper
from encryption import passwordHelper
import time
import sys
import getpass
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

class currentUser():
    def __init__ (self):
        '''
        initializing user login process and return a currentUser Object
        '''
        username = None
        password = None
        userloginArray = None
        fullUserArray = None

        for i in range(4, -1, -1):
            #limit to 5 try of password
            try:
                #trying to get username
                tryUsername = parser.stringParser("Please enter your username")
                #retrieving the user if exist to compare to PW
                usernameQuerry = SQLQuerry("SELECT username, passCode FROM Users WHERE username == ?")
                qResult = usernameQuerry.executeFetchAll(parameters=(tryUsername,))
                if tryUsername == '--quit':
                    break
                if len(qResult) != 1:
                    raise DBRecordError
                else:
                    username = tryUsername
                    userloginArray = qResult[0]
                    print("username correct")
                    break
            except DBRecordError:
                print(f"Invalid Username {i} attempts remaining")
        else:
            print("too many wrong username programming terminating ...")
            time.sleep(3)
            sys.exit(1)
        if tryUsername == '--quit':
            #catch the interruption of the user
            print("user Exit quitting")
            time.sleep(3)
            sys.exit(1)
        for i in range(4, -1, -1):
            try:
                #the PW is saved in hash so need to convert to hash to compare special parsing function becasue it will hide the needed 
                tryPW = passwordHelper.hashPW(getpass.getpass("Enter your password: "))
                #print(tryPW)
                #print(userloginArray[1])
                if tryPW == '--quit':
                    break
                if tryPW == userloginArray[1]:
                    #load encryption key if PW is correct
                    self.encryptionKey = encryptionHelper()
                    print("key loaded")
                    break
                else:
                    raise DBRecordError
            except DBRecordError:
                print(f"Invalid Password {i} attempts remaining")
        else:
            print("too many wrong username programming terminating ...")
            time.sleep(3)
            sys.exit(1)
        #catch the user terminaion
        if tryUsername == '--quit':
            print("user Exit quitting")
            time.sleep(3)
            sys.exit(1)
        #retrieving the full information from DATAbase instead of just the password for authentication
        fullUQuerry = SQLQuerry("SELECT ID, username, passCode, firstName, lastName, phoneNo, HomeAddress, postCode, UserType, deactivated  FROM Users WHERE username == ?")
        fullUserArray = fullUQuerry.executeFetchAll(decrypter=self.encryptionKey, parameters=('testGP',))
        #ifthe account is deactivated stop login
        if fullUserArray[0][9] == 'T':
            print('account deactivated please contact admin')
            time.sleep(3)
            sys.exit(1)
        #loading the user info into a state
        self.ID = fullUserArray[0][0]
        self.username = fullUserArray[0][1]
        self.passCode = fullUserArray[0][2]
        self.firstName = fullUserArray[0][3]
        self.lastName = fullUserArray[0][4]
        self.phoneNo = fullUserArray[0][5]
        self.HomeAddress = fullUserArray[0][6]
        self.postCode = fullUserArray[0][7]
        self.UserType = fullUserArray[0][8]
        self.deactivated = fullUserArray[0][9]

        


if __name__ == "__main__":
    # tryQuerry = SQLQuerry("SELECT ID, username, passCode, firstName, lastName, phoneNo, HomeAddress, postCode, UserType, deactivated  FROM Users WHERE username == ?")
    # EH = encryptionHelper()
    # result = tryQuerry.executeFetchAll(decrypter=EH, parameters=('testGP',))
    # print(result)
    user = currentUser()
    print(user.ID, user.username, user.passCode, user.firstName, user.lastName, user.phoneNo, user.HomeAddress, user.postCode, user.UserType, user.deactivated)
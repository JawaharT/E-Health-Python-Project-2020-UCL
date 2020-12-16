import os
from tabulate import tabulate
from parserHelp import parser
from login import currentUser
from databaseHelp import SQLQuerry
import time
import sys
import datetime


class AdminNavigator():
    """Admin class and attributes."""

    def mainNavigator(user):
        """
        :param parameters: current Admin info
        :return: divert user into the main admin functionalities
        """

        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print(f"Login Successsful. Hello {user.firstName}")
        userInfoTable = [("User Type:", user.UserType),
                         ("First Name: ", user.firstName),
                         ("Last Name: ", user.lastName),
                         ("Birthday: ", user.birthday),
                         ("Phone No: ", user.phoneNo),
                         ("Home Address: ", user.HomeAddress),
                         ("Post Code: ", user.postCode)]
        print(tabulate(userInfoTable))

        while True:
            userInput = parser.selectionParser(
                options={"D": "Delete/Deactivate existing GP", "G": "Add New GP", "P": "Add new Patient",
                         "--logout": "logout"})
            if userInput == "--logout":
                # reason for quitting is that it dumps the login info so the logout is complete and the key is not
                # accessible to future user.
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Logging you out ...")
                time.sleep(3)
                sys.exit(0)
            else:
                currentPage = userInput

            if currentPage == "D":
                currentPage = AdminNavigator.delete_GP(user)



    def delete_GP(self):
        """
        :return: updated table with the deleted GP record
        """
        # show all users that are deactivated for deletion
        allDeactivatedGPs = SQLQuerry("SELECT username FROM Users WHERE Deactivated = 'F' AND UserType= 'GP'")
        allDeactivatedGPsResult = allDeactivatedGPs.executeFetchAll(decrypter=user.encryptionKey, parameters=("username"))
        allDeactivatedGPsTable = []
        for nameIndex in range(len(allDeactivatedGPsResult)):
            allDeactivatedGPsTable.append([nameIndex+1, allDeactivatedGPsResult[nameIndex][0]])

        print(tabulate(allDeactivatedGPsTable, headers="Username"))

        # select a user from the table
        while True:
            print("Please match name exactly.")
            selectedGP = input("Write the name of GP to delete: ")
            if selectedGP not in allDeactivatedGPsTable:
                print("This name does not exist. Please try again.")
                continue
            else:
                # delete query, make sure to delete all presence of that user
                deleteQuery = SQLQuerry("DELETE FROM Users WHERE username == ?")
                newTable = deleteQuery.executeCommit()
                print(newTable)
                break


    def add_GP(self):
        pass

    def add_patient(self):
        pass


if __name__ == "__main__":
    user = currentUser(username="TestGP", encryptionKey="hkPN4iCVAG9_YIZ81pfzweqtwde6ea3jCdvUFTf6l_M=")
    AdminNavigator.mainNavigator(user)
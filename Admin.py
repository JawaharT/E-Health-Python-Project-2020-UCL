import os
from tabulate import tabulate

from encryption import encryptionHelper, passwordHelper
from login import currentUser, loginHelp
from parserHelp import parser
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
                continue



    def delete_GP(self):
        """
        :return: updated table with the deleted GP record
        """
        # show all users that are deactivated for deletion
        allDeactivatedGPs = SQLQuerry("SELECT username FROM Users WHERE Deactivated = 'T' AND UserType= 'GP'")

        allDeactivatedGPsResult = allDeactivatedGPs.executeFetchAll()
        allDeactivatedGPsTable, onlyGPs = [], []
        for nameIndex in range(len(allDeactivatedGPsResult)):
            onlyGPs.append(allDeactivatedGPsResult[nameIndex][0])
            allDeactivatedGPsTable.append([nameIndex+1, allDeactivatedGPsResult[nameIndex][0]])

        print(tabulate(allDeactivatedGPsTable, headers=("ID", "Username")))

        # select a user from the table
        while True:
            print("Please match name exactly. Press Enter to go back.")
            selectedGP = input("Write the name of GP to delete: ")
            if selectedGP == "":
                break
            if selectedGP not in onlyGPs:
                print("This name does not exist. Please try again.")
                continue
            else:
                # delete query, make sure to delete all presence of that user
                deleteQuery = SQLQuerry("DELETE FROM Users WHERE username=:who")
                deleteQuery.executeCommit({"who": selectedGP})
                print("Done.")
                break


    def add_GP(self):
        pass

    def add_patient(self):
        pass


if __name__ == "__main__":
    Q = SQLQuerry("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    EH = encryptionHelper()
    result = Q.executeCommit(("GP1",
                              "testGP1",
                              passwordHelper.hashPW("testGPPW2"),
                              EH.encryptToBits("1991-01-04"),
                              EH.encryptToBits("testGP1FitstName"),
                              EH.encryptToBits("testGP1LastName"),
                              EH.encryptToBits("0123450243"),
                              EH.encryptToBits("testGP1Home Address, test Road"),
                              EH.encryptToBits("AB1 7RT"),
                              "GP",
                              "T"))
    result = Q.executeCommit(("GP2",
                              "testGP2",
                              passwordHelper.hashPW("testGPPW3"),
                              EH.encryptToBits("1991-01-04"),
                              EH.encryptToBits("testGP2FitstName"),
                              EH.encryptToBits("testGP2LastName"),
                              EH.encryptToBits("0123450244"),
                              EH.encryptToBits("testGP2Home Address, test Road"),
                              EH.encryptToBits("AC1 7RT"),
                              "GP",
                              "T"))
    result = Q.executeCommit(("GP3",
                              "testGP3",
                              passwordHelper.hashPW("testGPPW"),
                              EH.encryptToBits("1991-01-04"),
                              EH.encryptToBits("testGP3FitstName"),
                              EH.encryptToBits("testGP3LastName"),
                              EH.encryptToBits("0123450289"),
                              EH.encryptToBits("testGP3Home Address, test Road"),
                              EH.encryptToBits("AD1 7RT"),
                              "GP",
                              "T"))

    # example admin user
    result = Q.executeCommit(("Admin12",
                              "testAdmin124",
                              passwordHelper.hashPW("testAdmin"),
                              EH.encryptToBits("1991-01-04"),
                              EH.encryptToBits("testAdminFitstName"),
                              EH.encryptToBits("testAdminLastName"),
                              EH.encryptToBits("0123450281"),
                              EH.encryptToBits("test Admin Home Address, test Road"),
                              EH.encryptToBits("AD4 7RT"),
                              "Admin",
                              "F"))
    loginParam = loginHelp.Login()
    user = currentUser(loginParam[0], loginParam[1])
    AdminNavigator.mainNavigator(user)
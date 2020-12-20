import os
from tabulate import tabulate

from encryption import encryptionHelper, passwordHelper
from login import currentUser, loginHelp
import getpass
from parserHelp import parser
from databaseHelp import SQLQuerry
import time
import sys


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
                options={"A": "View Records", "B": "Add New GP or Patient", "C": "Edit GP or Patient",
                         "D": "Delete Existing GP", "--logout": "logout"})
            if userInput == "--logout":
                # reason for quitting is that it dumps the login info so the logout is complete and the key is not
                # accessible to future user.
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Logging you out ...")
                time.sleep(3)
                sys.exit(0)
            else:
                currentPage = userInput

            if currentPage == "A":
                currentPage = AdminNavigator.viewRecords(user)
            elif currentPage == "B":
                currentPage = AdminNavigator.addGPPatient(user)
            elif currentPage == "C":
                currentPage = AdminNavigator.editGPPatient(user)
            elif currentPage == "D":
                currentPage = AdminNavigator.deleteGP(user)

    def viewRecords(self):
        """
        :return: User interface for viewing the desired records
        """
        while True:
            recordViewer = parser.selectionParser(
                options={"A": "View Patients", "B": "View GPs",
                         "C": "View Available Timeslots", "D": "View Patient Appointments",
                         "E": "View Patient Prescriptions", "--back": "back"})

            if recordViewer == "--back":
                return
            elif recordViewer == "A":
                query = SQLQuerry("SELECT Deactivated, ID, Username, birthday, firstName, lastName, phoneNo,"
                                  " HomeAddress, postCode FROM USERS WHERE UserType = 'Patient'")
                headers = ("Deactivated", "ID", "Username", "Birthday", "First Name", "Last Name", "PhoneNo", "Address",
                           "Postcode")
                startOfDecryption, decrypt = 3, True
            elif recordViewer == "B":
                query = SQLQuerry("SELECT Deactivated, ID, Username, birthday, firstName, lastName, phoneNo,"
                                  " HomeAddress, postCode FROM USERS WHERE UserType = 'GP'")
                headers = ("Deactivated", "ID", "Username", "Birthday", "First Name", "Last Name", "PhoneNo", "Address",
                           "Postcode")
                startOfDecryption, decrypt = 3, True
            elif recordViewer == "C":
                query = SQLQuerry("SELECT * FROM available_time")
                headers = ("StaffID", "Timeslot")
                startOfDecryption, decrypt = len(headers), False
            elif recordViewer == "D":
                query = SQLQuerry("SELECT * FROM Visit")
                headers = ("BookingNo", "NHSNo", "StaffID", "Timeslot", "Confirmed", "Attended", "Diagnosis", "Notes")
                startOfDecryption, decrypt = len(headers), False
            elif recordViewer == "E":
                query = SQLQuerry("SELECT * FROM prescription")
                headers = ("BookingNo", "DrugName", "Quantity", "Instructions")
                startOfDecryption, decrypt = len(headers), False
            else:
                print("Not a valid selection.\n")
                continue

            allData = query.executeFetchAll()
            EH = encryptionHelper()

            if len(allData) == 0:
                print("No records Available.\n")
                continue

            #print(tabulate(allData, headers))

            decryptedData = []
            for recordNumber in range(len(allData)):
                currentRecord = []
                if startOfDecryption != 0:
                    for notCryptedColumnNumber in range(0, startOfDecryption):
                        currentRecord.append(allData[recordNumber][notCryptedColumnNumber])
                # decrypting the encrypted data
                if decrypt:
                    for columnNumber in range(startOfDecryption, len(headers)):
                        currentRecord.append(EH.decryptMessage(allData[recordNumber][columnNumber]))
                decryptedData.append(currentRecord)

            print(tabulate(decryptedData, headers))
            print("Completed operation.\n")
            continue

    def deleteGP(self):
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

        if len(allDeactivatedGPsTable) == 0:
            print("No deactivated GPs available to delete.\n")
            return

        # select a deactivated GP account to delete
        while True:
            menu = parser.selectionParser(
                options={"A": "Delete GP", "--back": "back"})

            if menu == "--back":
                return
            elif menu == "A":
                print("Press Enter to delete.")
                selectedGP = input("Write the name of GP to delete: ")
                if selectedGP == "":
                    break
                if selectedGP not in onlyGPs:
                    print("This name does not exist. Please try again.\n")
                    continue
                else:
                # delete query, make sure to delete all presence of that user
                    deleteQuery = SQLQuerry("DELETE FROM Users WHERE username=:who")
                    deleteQuery.executeCommit({"who": selectedGP})
                    print("GP {0} deleted from Users table.\n".format(selectedGP))
                    return
            else:
                print("Not a valid selection.\n")
                continue

    def getCheckUserInput(self, parameterName, userGroup):
        """
        :param parameterName: The name of the paramter for Admin to enter
        :param userGroup: Patient or GP
        :return: New unique Username that is not currently being used
        """
        while True:
            parameter = input("Please enter {0} of {1}: ".format(parameterName, userGroup))
            # check if it exists in table, if it does ask again
            existsQuery = SQLQuerry("SELECT 1 FROM Users WHERE {0} =:who".format(parameterName)) \
                .executeCommit({"who": parameter})
            # print(existsQuery)
            if existsQuery > 0:
                print("{0} already exists. Please choose another.\n".format(parameterName))
                continue
            else:
                print("{0} approved.\n".format(parameterName))
                return parameter

    def registerNewPassword(self):
        """
        :return: check for valid new password that will match
        """
        while True:
            #password = input("Please enter Password: ")
            #passwordConfirm = input("Password confirmation: ")

            password = getpass.getpass("Enter new password: ")
            passwordConfirm = getpass.getpass("Enter new password again: ")
            if password != passwordConfirm:
                print("Passwords do not match. Please try again.\n")
            else:
                print("Passwords Match.\n")
                return passwordHelper.hashPW(password)

    def validLocalPhoneNumber(self):
        """
        :return: return a valid UK phone number
        """
        while True:
            phoneNumber = input("Please enter local UK phone number: ")
            if (len(phoneNumber.strip()) == 11) and \
                    (not any([char in phoneNumber for char in ["+", "-", "(", ")"]])):
                print("Valid Phone Number.\n")
                return encryptionHelper().encryptToBits(phoneNumber)
            else:
                print("Invalid Phone Number.Please try again.\n")

    def validPostcode(self):
        """
        :return: return a valid UK postcode
        """
        while True:
            tempPostcode = input("Please enter primary home postcode: ").strip().replace(" ", "")
            if (len(tempPostcode) != 5) and (len(tempPostcode) != 7):
                print("Invalid Postcode. Please try again.\n")
            else:
                print("Valid Postcode.\n")
                return encryptionHelper().encryptToBits(tempPostcode)

    def addGPPatient(self):
        """
        :return: updated table with new GP or patient record
        """
        while True:
            userGroup = input("Please enter type of user (GP or Patient): ").lower().strip()
            if userGroup == "gp":
                newID = parser().GPStaffNoParser()
                userGroup = userGroup.upper()
                break
            elif userGroup == "patient":
                newID = parser().nhsNoParser()
                userGroup = userGroup[0].upper()+userGroup[1:]
                break
            else:
                print("Incorrect input. Please Try again.\n")
                continue

        #print(userGroup)
        username = AdminNavigator.getCheckUserInput(user, "username", userGroup)
        password = AdminNavigator.registerNewPassword(user)

        birthday = encryptionHelper().encryptToBits(str(parser().dateParser("Please enter birthday: ", False).date()))
        firstName = encryptionHelper().encryptToBits(input("Please enter first name: "))
        lastName = encryptionHelper().encryptToBits(input("Please enter last name: "))

        # check for only local phone numbers and 11 digits only
        telephone = AdminNavigator.validLocalPhoneNumber(user)
        address = encryptionHelper().encryptToBits(input("Please enter primary home address (one line): "))

        # check for only 5 or 7 chars
        postcode = AdminNavigator.validPostcode(user)

        Q = SQLQuerry("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        Q.executeCommit((newID, username, password, birthday, firstName, lastName, telephone, address, postcode,
                         userGroup, "F"))
        print("Successfully Added to Database. Going back to home page.\n")
        return

    def updateParameterRecord(self, selectedUser, parameter, newParameterValue):
        editQ = SQLQuerry("UPDATE Users SET {0} = ? WHERE username= ?".format(parameter))
        editQ.executeCommit((newParameterValue, selectedUser))

    def editGPPatient(self):
        """
        :return: Edit existing GP or Patient Record
        """
        #show all GPs and Patients
        viewallGPsandPatients = SQLQuerry("SELECT username FROM Users WHERE UserType= 'GP' or 'Patient'")

        viewallGPsandPatientsResult = viewallGPsandPatients.executeFetchAll()

        if len(viewallGPsandPatientsResult) == 0:
            print("No Patients or GPs registered. Please add before coming back.\n")
            return

        viewallGPsandPatientsTable, GPandPatient,usertype = [], [], []
        for nameIndex in range(len(viewallGPsandPatientsResult)):
            GPandPatient.append(viewallGPsandPatientsResult[nameIndex][0])
            viewallGPsandPatientsTable.append([nameIndex + 1, viewallGPsandPatientsResult[nameIndex][0]])

        print(tabulate(viewallGPsandPatientsTable, headers=("ID", "Username", "Usertype")))

        # select a user from the table
        while True:
            editmenu = parser.selectionParser(
                options={"A": "Edit GP or Patient", "--back": "back"})
            if editmenu == "--back":
                return
            elif editmenu == "A":
                print("Press enter to go back.")
                selectedUser = input("Enter the username to edit the profile: ")
                if selectedUser == "":
                    break
                if selectedUser not in GPandPatient:
                    print("This username does not exist. Please enter a valid username.\n")
                    continue
                else:
                    recordEditor = parser.selectionParser(
                        options={"A": "Update Password", "B": "Update Birthday",
                             "C": "Update Firstname", "D": "Update Lastname",
                             "E": "Update Phone Number","F":"Update Home Address","G":"Update Postcode",
                             "--back": "back"})

                    if recordEditor == "--back":
                        return
                    elif recordEditor == "A":
                        newParameterValue = AdminNavigator.registerNewPassword(user)
                        parameter = "passCode"
                    elif recordEditor == "B":
                        # newbirthday = parser().dateParser("Please enter birthday: ", allowback=False)
                        newParameterValue = encryptionHelper().encryptToBits(
                            str(parser().dateParser("Please enter birthday: ", False).date()))
                        parameter = "birthday"
                    elif recordEditor == "C":
                        newParameterValue = encryptionHelper().encryptToBits(input("Please enter new first name: "))
                        parameter = "firstName"
                    elif recordEditor == "D":
                        newParameterValue = encryptionHelper().encryptToBits(input("Please enter new last name: "))
                        parameter = "lastName"
                    elif recordEditor == "E":
                        newParameterValue = AdminNavigator.validLocalPhoneNumber(user)
                        parameter = "phoneNo"
                    elif recordEditor == "F":
                        newParameterValue = encryptionHelper().encryptToBits(input("Please enter primary home address (one line): "))
                        parameter = "HomeAddress"
                    else:
                        newParameterValue = AdminNavigator.validPostcode(user)
                        parameter = "postCode"

                    AdminNavigator.updateParameterRecord(user, selectedUser, parameter, newParameterValue)
                    print("Successfully Update to Database. Going back to home page.\n")
                    return


if __name__ == "__main__":
    """Q = SQLQuerry("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
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
 #example Admin
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
                              "F"))"""
    loginParam = loginHelp.Login()
    user = currentUser(loginParam[0], loginParam[1])
    AdminNavigator.mainNavigator(user)
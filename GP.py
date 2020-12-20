import os
from tabulate import tabulate
from parserHelp import parser
from login import currentUser
from databaseHelp import SQLQuerry
import time
import sys
import datetime





class GPNavigator():
    """
    GP option for navigation
    """
    @staticmethod
    def mainNavigator(user):
        """
        it will print the user information !!you might want to reuse it
        then divert the user int the 3 main function ofGP Add/view avaliability, confirm/view bookings, start the process of viewing patient
        """
        while True:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print(f"Login Successful. Hello {user.firstName}")
            userInfoTable = [["User Type:", user.UserType],
                            ["First Name: ", user.firstName],
                            ["Last Name: ", user.lastName],
                            ["Birthday: ", user.birthday],
                            ["Phone No: ", user.phoneNo],
                            ["Home Address: ", user.HomeAddress],
                            ["Post Code: ", user.postCode]
                            ]
            print(tabulate(userInfoTable))
            userInput = parser.selectionParser(options={"A": "add/View availability","C": "Confirm/view bookings","V": "View/Start appointment","--logout": "logout"})
            if userInput == "--logout":
                #reason for quitting is that it dumps the login info so the logout is complete and the key is not accessible to futureuser.
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Logging you out ...")
                time.sleep(3)
                sys.exit(0)
            else:
                currentPage = userInput
        
            if currentPage == "A":
                currentPage = GPNavigator.avaliabilityAorRM(user)
            if currentPage == "C":
                currentPage = GPNavigator.confirmBooking(user)
            if currentPage == "V":
                #add your function to here
                currentPage = GPNavigator.viewAppointment(user)
                pass

    @staticmethod
    def avaliabilityAorRM(user):
        """
        step 2 in beanch A ask which date the user wish to manipulte ->
        Display the schedule of avaliability of the date ->
        ask to add or remove avaliability -> divert to subfunction adding or removing
        """
        stage = 0
        selectedDate = None
        while True:
            while stage == 0:
                #rander the prompt to ask for the date
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                dateInput = parser.dateParser(question="Select a Date:")
                
                if dateInput == "--back":
                    #if --back is inputted, it will return to the main window of GP
                    return "main"
                else:
                    selectedDate = dateInput
                    stage = 1
            while stage == 1:
                #randering the table of available schedule
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                #retrieving info from DB
                Qaval = SQLQuerry("SELECT StaffID, Timeslot FROM available_time WHERE StaffID = ? AND Timeslot >= ? AND Timeslot <= ?",)
                selectedDatePlus1 = selectedDate + datetime.timedelta(days=1)
                Qavalresult = Qaval.executeFetchAll(parameters = (user.ID, selectedDate, selectedDatePlus1))
                #storing a raw version of the important data as it is easier for the sqlite package to handle it 
                QavalTableRaw = []
                #for display purposes it is better to minupulate it
                QavalTable = []
                for i in range(len(Qavalresult)):
                    QavalTable.append([i+1, str(Qavalresult[i][1])])
                    QavalTableRaw.append([i+1, Qavalresult[i][1]])
                print(f"You are viewing your schedule of: {selectedDate.strftime('%Y-%m-%d')}")
                print(tabulate(QavalTable, headers=["Pointer", "timeslot"]))
                userInput = parser.selectionParser(options={"A": "add availability","R": "remove availability","--back": "back to previous page"})
                if userInput == "--back":
                    #breaking into the previous stage of date selection
                    stage = 0
                    break
                elif userInput == "A":
                    #divert to adding availability
                    stage = 1
                    GPNavigator.addAvailability(selectedDate, user)
                    break
                elif userInput == "R":
                    #divert to removing availability
                    GPNavigator.rmAvailability(QavalTableRaw, user)
                    stage = 1
    def rmAvailability(QavalTableRaw, user):
        """
        function to prompt the user f which entry to remove -> parsing the input
        returning the info of the one they want to remove -> executing eansection
        """
        slotToRm = []
        while True:
            selectedEntry = parser.listNumberParser("Select the entry to remove", (1,len(QavalTableRaw)+1))
            if selectedEntry == '--back':
                return "main"
            for row in QavalTableRaw:
                if row[0] in selectedEntry:
                    slotToRm.append(row[1])
            print("These time slot will be removed and made unavailable")
            print(tabulate(map(str, slotToRm)))
            confirm = parser.selectionParser(options={"Y": "confirm", "N":"go back and select again"})
            if confirm == "Y":
                insertAvalQuerry = SQLQuerry("DELETE FROM available_time WHERE StaffID = ? AND Timeslot = ?")
                try:
                    for slot in slotToRm:
                        insertAvalQuerry.executeCommit((user.ID, slot))
                    print("removed")
                    time.sleep(3)
                    return
                except:
                    print("Error encountered")
                    slotToRm = []
                    time.sleep(3)
                    print("restarting")
            if confirm == "N":
                print("action canceled returning...")
                time.sleep(3)
                break            

    def addAvailability(selectedDate, user):
        """
        function to prompt user to enter te start of their availability after that te ending time, 
            for GP they usually know their shift in advance so they will add their avaliable time into the table.
        executing the INSERT transaction
        """

        stage = 0
        selectedStart = None
        selectedEnd = None
        slotToAdd = []
        while True:
            while stage == 0:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Each timeslot will be 15min long")
                startTime = parser.timeParser("Enter the hour you wish to start taking appiontmets:")
                selectedDate
                if startTime == "--back":
                    return None
                else:
                    selectedStart = datetime.datetime.combine(selectedDate.date(), startTime.time())
                    stage = 1
            while stage == 1:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Each timeslot will be 15 min long")
                print(f"you wish to start from {str(selectedStart)}")
                endTime = parser.timeParser("Enter the hour you wish to start taking appiontmets:")
                selectedDate
                if endTime == "--back":
                    stage = 0
                    break
                else:
                    selectedEnd = datetime.datetime.combine(selectedDate.date(), endTime.time())
                    stage = 2
                    break
            while stage == 2:
                currentTime = selectedStart
                while currentTime < selectedEnd:
                    slotToAdd.append(currentTime)
                    currentTime = currentTime + datetime.timedelta(minutes=15)
                print("These are the slot that you wish to add:")
                print(tabulate(map(str, slotToAdd)))
                confirm = parser.selectionParser(options={"Y": "confirm", "N":"go back and select again"})
                if confirm == "Y":
                    insertAvalQuerry = SQLQuerry("INSERT INTO available_time VALUES (?, ?)")
                    try:
                        for slot in slotToAdd:
                            insertAvalQuerry.executeCommit((user.ID, slot))
                        print("adding")
                        return
                    except:
                        print("invalid timeslot. some of the timeslot is already in the table Please Retry")
                        stage = 0
                        selectedStart = None
                        selectedEnd = None
                        slotToAdd = []
                        time.sleep(3)
                        print("restarting")
                        break
                if confirm == "N":
                    stage = 0
                    selectedStart = None
                    selectedEnd = None
                    slotToAdd = []
                    print("restarting")
                    break
    @staticmethod
    def confirmBooking(user):
        """
        first step of branch C confirm booking
        similar to branch A can also be reused in branch V
        ask for date -> display the bookings from patients ->
        ask for which entry the user wish to modifly
        -> return to previous function | pass to teansactions
        """
        stage = 0
        selectedDate = None
        while True:
            while stage == 0:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                dateInput = parser.dateParser(question="Select a Date:")
                if dateInput == "--back":
                    return "main"
                else:
                    selectedDate = dateInput
                    stage = 1
            while stage == 1:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                Qtext = "SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, users.lastName, visit.Confirmed "
                Qtext += "FROM visit INNER JOIN users ON visit.NHSNo = users.ID "
                Qtext += "WHERE visit.StaffID = ? AND visit.Timeslot >= ? AND visit.Timeslot <= ?"
                print(Qtext)
                Qbooked = SQLQuerry(Qtext)
                selectedDatePlus1 = selectedDate + datetime.timedelta(days=1)
                Qbookedresult = Qbooked.executeFetchAll(decrypter=user.encryptionKey, parameters = (user.ID, selectedDate, selectedDatePlus1))
                QbookedTableRaw = []
                QbookedTable = []
                translation = {"T":"Accepted", "F": "Rejected", "P": "Pendig Response"}
                for i in range(len(Qbookedresult)):
                    QbookedTable.append([i+1, Qbookedresult[i][0],str(Qbookedresult[i][1]), Qbookedresult[i][2], Qbookedresult[i][3],Qbookedresult[i][4], translation[Qbookedresult[i][5]]])
                    QbookedTableRaw.append([i+1, Qbookedresult[i][0], Qbookedresult[i][1]])
                print(f"You are viewing your bookings of: {selectedDate.strftime('%Y-%m-%d')}")
                print(tabulate(QbookedTable, headers=["Pointer", "BookingNo", "timeslot", "Patient NHSNo", "P. First Name", "P. Last Name", "Confirmed"]))
                selectEntryNo = parser.integerParser(question="Select Entry using number")

                print(selectEntryNo)
                if selectEntryNo == "--back":
                    stage = 0
                    break
                selectedRow = QbookedTable[selectEntryNo-1]
                #print(selectedRow)
                selectedRowRaw = QbookedTableRaw[selectEntryNo-1]
                GPNavigator.bookingTransaction(selectedRow, selectedRowRaw, user)

    def bookingTransaction(selectedRow, selectedRowRaw, user):
            """
            transaction of the booking confirmation
            ask the user whether they wish to confirm or reject it
            for confirm it will automatically reject all bookings in the same time slot
            for reject no other step required 
            """
            while True:
                print("You selected this row")
                print(tabulate([selectedRow], headers=["Pointer", "BookingNo", "timeslot", "Patient NHSNo", "P. First Name", "P. Last Name", "Confirmed"]))
                userInput = parser.selectionParser(options={"C": "Confirm","R": "Reject","--back": "back to previous page"})
                if userInput == "--back":
                    return
                elif userInput == "C":
                    stage = 1
                    print("Warning! this will reject all other bookings in the same timeslot")
                    userInputYN = parser.selectionParser(options={"Y": "Confirm","N": "Rollback"})
                    if userInputYN == 'N':
                        break
                    else:
                        QuerryReject = SQLQuerry("UPDATE Visit SET Confirmed = 'F' WHERE StaffID = ? AND Timeslot = ?")
                        exeQuerryReject = QuerryReject.executeCommit((user.ID, selectedRowRaw[2]))
                        QuerryAccept = SQLQuerry("UPDATE Visit SET Confirmed = 'T' WHERE BookingNo = ?")
                        exeQuerryAccept = QuerryAccept.executeCommit((selectedRowRaw[1],))
                    break
                elif userInput == "R":
                        QuerryReject = SQLQuerry("UPDATE Visit SET Confirmed = 'F' WHERE BookingNo = ?")
                        exeQuerryReject = QuerryReject.executeCommit((selectedRowRaw[1],))
                        return

    @staticmethod
    def viewAppointment(user):
        """
        step 1 in branch v ask which date the user wish to manipulte ->
        Display confirmed appointment of the date ->

        """
        stage = 0
        selectedDate = None
        while True:
            while stage == 0:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                dateInput = parser.dateParser(question="Select a Date:")
                if dateInput == "--back":
                    return "main"
                else:
                    selectedDate = dateInput
                    stage = 1
            while stage == 1:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                Qtext = "SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, users.lastName, visit.Confirmed "
                Qtext += "FROM visit INNER JOIN users ON visit.NHSNo = users.ID "
                Qtext += "WHERE visit.StaffID = ? AND visit.Timeslot >= ? AND visit.Timeslot <= ? AND visit.Confirmed = 'T' "
                #print(Qtext)
                Qbooked = SQLQuerry(Qtext)

                selectedDatePlus1 = selectedDate + datetime.timedelta(days=1)
                Qbookedresult = Qbooked.executeFetchAll(decrypter=user.encryptionKey, parameters = (user.ID, selectedDate, selectedDatePlus1))
                QbookedTableRaw = []
                QbookedTable = []
                translation = {"T":"Accepted", "F": "Rejected", "P": "Pending Response"}
                for i in range(len(Qbookedresult)):
                    QbookedTable.append([i+1, Qbookedresult[i][0],str(Qbookedresult[i][1]), Qbookedresult[i][2], Qbookedresult[i][3],Qbookedresult[i][4], translation[Qbookedresult[i][5]]])
                    QbookedTableRaw.append([i+1, Qbookedresult[i][0], Qbookedresult[i][2]])
                print(f"You are viewing all of your confirmed bookings of: {selectedDate.strftime('%Y-%m-%d')}")
                print(tabulate(QbookedTable, headers=["Pointer", "BookingNo", "timeslot", "Patient NHSNo", "P. First Name", "P. Last Name", "Confirmed"]))
                # print(tabulate(QbookedTableRaw, headers=["Pointer", "BookingNo", "Patient NHSNo"]))
                selectEntryNo = parser.integerParser(question="Select Entry using number or input '--back' for back")
                print(selectEntryNo)
                if selectEntryNo == "--back":
                    stage = 0
                    break
                #selectedRow = QbookedTable[selectEntryNo-1]
                #print(selectedRow)
                # selectedNhsNo = QbookedTableRaw[selectEntryNo-1][2]
                # print(selectedNhsNo)

                selectedBookingNo=QbookedTableRaw[selectEntryNo-1][1]
                print(selectedBookingNo)

                GPNavigator.chooseAppointment(selectedBookingNo, user)
    
    @staticmethod
    def chooseAppointment(selectedBookingNo, user):
            """
            step 2 in branch v
            show details of selected patient  ->
            ask the user whether they wish to change it ->
            for D and N they can change diagnosis or notes ->
            for P they can add or remove prescription
            """

            while True:

                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                Qtext = "SELECT visit.BookingNo, visit.Timeslot, visit.NHSNo, users.firstName, users.lastName, visit.Confirmed, users.birthday, users.phoneNo, users.HomeAddress, users.postcode, visit.diagnosis, visit.notes "
                Qtext += "FROM visit INNER JOIN users ON visit.NHSNo = users.ID "
                Qtext += "WHERE visit.BookingNo = ? "
                Qbooked = SQLQuerry(Qtext)
                Qbookedresult = Qbooked.executeFetchAll(decrypter=user.encryptionKey, parameters = (selectedBookingNo,))
                print(tabulate([Qbookedresult[0][:-3]], headers=["BookingNo", "timeslot", "Patient NHSNo",  "P. First Name", "P. Last Name", "Confirmed", "birthday", "phoneNo", "HomeAddress", "postcode"]))
                print("----------")
                print("Diagnosis:")
                print("----------")
                print(Qbookedresult[0][10])
                print("----------")
                print("Notes:")
                print("----------")
                print(Qbookedresult[0][11])
                print("-------------")
                print("Prescription:")
                print("-------------")
                Qtext = "SELECT drugName, quantity, instructions "
                Qtext += "FROM prescription WHERE BookingNo = ? "
                Qprescription = SQLQuerry(Qtext)
                Qprescriptionresult = Qprescription.executeFetchAll(decrypter=user.encryptionKey,parameters=(selectedBookingNo,))
                QprescriptionresultTable = []
                for i in range(len(Qprescriptionresult)):
                    QprescriptionresultTable.append([i+1, Qprescriptionresult[i][0], Qprescriptionresult[i][1],  Qprescriptionresult[i][2]])
                print(tabulate(QprescriptionresultTable, headers=["ItemNo", "Drug Name", "Qanntity", "Instrctions"]))
                print("--------------")
                userInput = parser.selectionParser(options={"D": "add diagnosis", "N": "add notes", "P": " edit prescription", "--back": "back to previous page"})
                if userInput == "--back":
                    return
                elif userInput == "D":
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                    print(f"Here is your diagnosis for Booking Number {Qbookedresult[0][0]}")
                    print("----------")
                    print("Diagnosis:")
                    print("----------")
                    print(Qbookedresult[0][10])
                    QuerryDiagnosis = SQLQuerry(" UPDATE Visit SET diagnosis = ? WHERE BookingNo = ? ")

                    diagnosisInput = parser.stringParser("Please enter your diagnosis:")

                    exeQuerryDiagnosis = QuerryDiagnosis.executeCommit((diagnosisInput, Qbookedresult[0][0]))
                    print("Your diagnosis has been given, you are going back to the patient info page...")

                elif userInput == "N":
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                    print(f"Here is your note for Booking Number {Qbookedresult[0][0]}")
                    print("----------")
                    print("Notes:")
                    print("----------")
                    print(Qbookedresult[0][11])
                    QuerryDiagnosis = SQLQuerry(" UPDATE Visit SET notes = ? WHERE NHSNo = ? ")
                    #notesInput = input("Please enter your notes:\n")
                    notesInput = parser.stringParser("Please enter your notes:")
                    # print(notesInput)
                    exeQuerryNotes = QuerryDiagnosis.executeCommit((notesInput, Qbookedresult[0][0]))
                    print("Your notes has been given,you are going back to the patient info page...")

                elif userInput == "P":
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                    print(f"Here is your Prescription for Booking Number {Qbookedresult[0][0]}")
                    print("-------------")
                    print("Prescription:")
                    print("-------------")
                    print(tabulate(QprescriptionresultTable, headers=["ItemNo", "Drug Name", "Qanntity", "Instrctions"]))

                    userInput = parser.selectionParser(options={"A": "add prescription", "R": "remove prescription", "--back": "back to previous page"})
                    if userInput == "--back":
                        return
                    elif userInput == "A":
                        os.system('cls' if os.name == 'nt' else "printf '\033c'")
                        Querryprescription = SQLQuerry(" INSERT INTO prescription (BookingNo, drugName, quantity, instructions) VALUES (?, ?, ?, ?)  ")
                        #BookingNo = input("Please enter your BookingNo:\n")
                        # print(notesInput)
                        #drugName = input("Please enter your drugName:\n")
                        drugName = parser.stringParser("Please enter your drugname:")
                        #quantity = input("Please enter your quantity:\n")
                        quantity = parser.stringParser("Please enter your quantity:")
                        #instructions = input("Please enter your instructions:\n")
                        instructions = parser.stringParser("Please enter your instructions:")

                        exeQuerryprescription = Querryprescription.executeCommit((Qbookedresult[0][0], drugName, quantity, instructions))
                        print("Your prescription has been given,you are going back to the patient info page...")

                    elif userInput == "R":
                        GPNavigator.removePrescripion(Qbookedresult[0][0], QprescriptionresultTable)
                        
    @staticmethod
    def removePrescripion(BookingNo, QprescriptionresultTable):
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print(f"Here is your Prescription for Booking Number {BookingNo}")
        print("-------------")
        print("Prescription:")
        print("-------------")
        print(tabulate(QprescriptionresultTable, headers=["ItemNo", "Drug Name", "Qanntity", "Instrctions"]))
        Querryprescription = SQLQuerry(" DELETE FROM prescription WHERE BookingNo = ? AND drugName = ? ")
        selectItemNo = parser.integerParser(question="Select Item using number")
        if selectItemNo == "--back":
            return
        # print(notesInput)
        exeQuerryprescription = Querryprescription.executeCommit((BookingNo, QprescriptionresultTable[selectItemNo-1][1]))
        print("this prescription has been removed,you are going back to the patient info page...")
        return

if __name__ == "__main__":
    user = currentUser()
    GPNavigator.mainNavigator(user)           

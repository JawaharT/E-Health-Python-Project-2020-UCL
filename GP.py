import os
from tabulate import tabulate
from parserHelp import parser
from login import currentUser
from databaseHelp import SQLQuerry
import time
import sys
import datetime

class GPNavigator():
    """GP option for navigation"""
    @staticmethod
    def mainNavigator(user):
        currentPage = "main"
        while currentPage == "main":
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print(f"Login Successsful. Hello {user.firstName}")
            userInfoTable = [("User Type:", user.UserType),
                        ("First Name: ", user.firstName),
                        ("Last Name: ", user.lastName),
                        ("Phone No: ", user.phoneNo),
                        ("Home Address: ", user.HomeAddress),
                        ("Post Code: ", user.postCode)
                        ]
            print(tabulate(userInfoTable))
            userInput = parser.selectionParser(options={"A": "add availability","C": "confirm bookings","S": "start appointment","--logout": "logout"})
            if userInput == "--logout":
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print("Logging you out ...")
                time.sleep(3)
                sys.exit(0)
            else:
                currentPage = userInput
        
        if currentPage == "A":
            currentPage = GPNavigator.avaliabilityAorRM(user)

    @staticmethod
    def avaliabilityAorRM(user):
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
                Qaval = SQLQuerry("SELECT StaffID, Timeslot FROM available_time WHERE StaffID = ? AND Timeslot >= ? AND Timeslot <= ?",)
                selectedDatePlus1 = selectedDate + datetime.timedelta(days=1)
                Qavalresult = Qaval.executeFetchAll(parameters = (user.ID, selectedDate, selectedDatePlus1))
                QavalTableRaw = []
                QavalTable = []
                for i in range(len(Qavalresult)):
                    QavalTable.append([i+1, str(Qavalresult[i][1])])
                    QavalTableRaw.append([i+1, Qavalresult[i][1]])
                print(f"You are viewing your schedule of: {selectedDate.strftime('%Y-%m-%d')}")
                print(tabulate(QavalTable, headers=["Pointer", "timeslot"]))
                userInput = parser.selectionParser(options={"A": "add availability","R": "remove availability","--back": "back to previous page"})
                if userInput == "--back":
                    stage = 0
                    break
                elif userInput == "A":
                    stage = 1
                    GPNavigator.addAvailability(selectedDate, user)
                    break
                elif userInput == "R":
                    GPNavigator.rmAvailability(QavalTableRaw, user)
                    stage = 1
    def rmAvailability(QavalTableRaw, user):
        slotToRm = []
        while True:
            selectedEntry = parser.listNumberParser("Select the entry to remove", (1,len(QavalTableRaw)+1))
            if selectedEntry == '--back':
                return
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



        
            

                

if __name__ == "__main__":
    user = currentUser()
    GPNavigator.mainNavigator(user)           

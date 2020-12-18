"""Main Program here."""
import databaseHelp
from login import currentUser
from parserHelp import parser
import time

from parserHelp import parser

from GP import GPNavigator

from Admin import AdminNavigator

def checkUsername(): # i puttd it in a class
    """Check if username is valid."""
    while True:
        username = input("Enter Username: ")
        queryHelper = databaseHelp.SQLQuerry("SELECT 1 FROM Users WHERE USERNAME = {0}".format(username))

        try:
            if queryHelper.executeFetchAll() is not None:
                print("Found username.")
                break
            else:
                print("Not found/does not exist. Please try again.")
                continue
        except Exception as e:
            print(e)
            break
        """
        try:
            cursor = dbconn.cursor()
            cursor.execute("SELECT 1 FROM {0} WHERE USERNAME = ?".format(usertype), (username,))
            if cursor.fetchone() is not None:
                print("Found username and repeat process for password, before login.")
                break
            else:
                print("Not found/does not exist. Please try again.")
                continue
        # database connection issue
        except sqlite3.Error as e:
            print(e)
            break
        """

if __name__ == '__main__':
    # Exception handling if database not present/cannot connect
    #conn = create_connection("GPDB.db")
    #checkUsername(conn, "Users")
    #if conn:
    #    conn.close()

    #newDatabase = databaseHelp.database()
    #conn = newDatabase.create_connection()
    #checkUsername()
    while True:
        print("Wellcome to Group 6 GP System")
        loginOrRegster = parser.selectionParser(options={"R":"register", "L":"login","--quit":"quit"})
        user = None
        if loginOrRegster == 'L':

            loginParam = loginHelp.Login()
            if loginParam != False:
                user = currentUser(loginParam[0], loginParam[1])
                if user.UserType == "GP":
                    GPNavigator.mainNavigator(user)
                elif user.UserType == "Admin":
                    AdminNavigator.mainNavigator(user)

            
        elif loginOrRegster == 'R':
            #not done
            print("register")
            quit()
        elif loginOrRegster == "--quit":
            print("quitting...")
            time.sleep(3)
            SystemExit(1)

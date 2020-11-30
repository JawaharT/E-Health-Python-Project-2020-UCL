"""Main Program here."""
import sqlite3


def getConnection():
    """"""
    dbconn = None
    try:
        dbconn = sqlite3.connect("database.db")
    except sqlite3.Error as e:
        print(e)
    return dbconn


def checkPatientUsername(dbconn):
    """"""
    username = input("Enter Username: ")

    cursor = dbconn.cursor()
    cursor.execute("select username from patients")
    records = cursor.fetchall()

    for record in records[0]:
        if username in record:
            print("Found username.")
        else:
            print("Not found/does not exist.")


if __name__ == '__main__':
    conn = getConnection()
    checkPatientUsername(conn)

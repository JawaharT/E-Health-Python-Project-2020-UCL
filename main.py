"""Main Program here."""
from CreateDatabase import create_connection


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
    conn = create_connection("database.db")
    checkPatientUsername(conn)

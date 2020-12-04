"""Main Program here."""
from CreateDatabase import create_connection


def checkPatientUsername(dbconn):
    """"""
    username = input("Enter Username: ")

    cursor = dbconn.cursor()
    cursor.execute("select exists (select 1 from patients where username = ?)", (username,))

    if cursor.fetchone():
        print("Found username.")
    else:
        print("Not found/does not exist.")


if __name__ == '__main__':
    conn = create_connection("database.db")
    checkPatientUsername(conn)

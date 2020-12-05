"""Main Program here."""
from CreateDatabase import create_connection
import sqlite3


def checkUsername(dbconn, usertype):
    """Check if username is valid."""
    while True:
        username = input("Enter Username: ")

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


if __name__ == '__main__':
    # Exception handling if database not present/cannot connect
    conn = create_connection("GPDB.db")
    checkUsername(conn, "Users")
    if conn:
        conn.close()

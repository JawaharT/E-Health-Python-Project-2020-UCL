"""Main Program here."""
from CreateDatabase import create_connection


def checkUsername(dbconn, usertype):
    """"""
    while True:
        username = input("Enter Username: ")

        cursor = dbconn.cursor()
        cursor.execute("SELECT 1 FROM {0} WHERE USERNAME = ?".format(usertype), (username,))
        if cursor.fetchone() is not None:
            print("Found username and repeat process for password, before login.")
            break
        else:
            print("Not found/does not exist. Please try again.")
            continue


if __name__ == '__main__':
    # Exception handling if database not present/cannot connect
    conn = create_connection("database.db")
    checkUsername(conn, "patients")
    checkUsername(conn, "GPs")
    checkUsername(conn, "admins")
    if conn:
        conn.close()

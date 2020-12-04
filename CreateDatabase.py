# import sqlite3


# # Fix: May create duplicates if ran more tha once.

# def create_connection(db_file):
#     """Create a database connection to the SQLite database
#         specified by db_file
#     :param db_file: database file
#     :return: Connection object or None"""
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except sqlite3.Error as e:
#         print(e)

#     return conn


# def create_table(conn, create_table_sql):
#     """Create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement"""
#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except sqlite3.Error as e:
#         print(e)


# def createAdmins(conn, admin):
#     """Create admins in Admin table."""
#     sql = ''' INSERT INTO admins(first_name, last_name, username, password) VALUES(?,?,?,?)'''
#     cur = conn.cursor()
#     cur.execute(sql, admin)
#     conn.commit()
#     return cur.lastrowid


# def createPatients(conn, patient):
#     """Create Patients in Patient table."""
#     sql = ''' INSERT INTO patients(first_name, last_name, username, password) VALUES(?,?,?,?)'''
#     cur = conn.cursor()
#     cur.execute(sql, patient)
#     conn.commit()
#     return cur.lastrowid


# def createGPs(conn, gp):
#     """Create GPs in GP table."""
#     sql = ''' INSERT INTO GPs(first_name, last_name, username, password) VALUES(?,?,?,?)'''
#     cur = conn.cursor()
#     cur.execute(sql, gp)
#     conn.commit()
#     return cur.lastrowid


# def main():
#     """Create database with 3 tables and store it inside database.db"""
#     database = "database.db"

#     sql_create_admins_table = """CREATE TABLE IF NOT EXISTS admins (
#                                         admin_id integer PRIMARY KEY,
#                                         first_name text NOT NULL,
#                                         last_name text NOT NULL,
#                                         username text NOT NULL,
#                                         password test NOT NULL); """

#     sql_create_patients_table = """CREATE TABLE IF NOT EXISTS patients (
#                                     patient_id integer PRIMARY KEY,
#                                     first_name text NOT NULL,
#                                     last_name text NOT NULL,
#                                     username text NOT NULL,
#                                     password test NOT NULL);"""

#     sql_create_gps_table = """CREATE TABLE IF NOT EXISTS GPs (
#                                         GP_id integer PRIMARY KEY,
#                                         first_name text NOT NULL,
#                                         last_name text NOT NULL,
#                                         username text NOT NULL,
#                                         password test NOT NULL);"""

#     # create a database connection
#     conn = create_connection(database)

#     # create tables
#     if conn is not None:
#         # Create Admins Table
#         create_table(conn, sql_create_admins_table)

#         # Create Patients Table
#         create_table(conn, sql_create_patients_table)

#         # Create GPs Table
#         create_table(conn, sql_create_gps_table)

#         # Add records to tables
#         admin = ("Admin1", "Darwin", "darwinian", "not encrypted")
#         # Retrieve id from record
#         admin1_id = createAdmins(conn, admin)

#         createPatients(conn, ("Patient1", "Patient1 Last name", "Patient 1 username", "not encrypted yet"))
#         createGPs(conn, ("GP1", "GP1 Last name", "GP1 username", "not encrypted yet"))
#     else:
#         print("Cannot create the connection to database.")


# if __name__ == '__main__':
#     main()

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    file -> None 
    create a database connection to a SQLite database 
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def executeSQLScript(SQLScriptPath, db_file):
    '''
    file -> None 
    Execute sqlscript file 
    '''
    SQLfile = open(SQLScriptPath, mode='r')
    SQLScript = SQLfile.read()
    print(SQLScript)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.executescript(SQLScript)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        SQLfile.close

if __name__ == '__main__':
    db_name = "GPDB.db"
    create_connection(db_name)
    executeSQLScript("GPDB.sql", db_name)


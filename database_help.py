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
#     t
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
from encryption import EncryptionHelper
from encryption import PasswordHelper


class Database:
    """
    class for data base connection
    """
    def __init__(self, db_file="GPDB.db"):
        """
        :param db_file: path to sqlite DB file, default GPDB.db (str)
        specify the db to be used in db_file
        """
        self.db_file = db_file

    def create_connection(self):
        """
        create a database / test connection to a SQLite database 
        :return conn: return connected db
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            # print(sqlite3.version)
        except Error as e:
            print(e)

        return conn
    
    @staticmethod
    def close_connection(conn):
        """
        :param conn: connection object of SQL
        closing the connection to db
        """
        if conn:
            conn.close()

    def executeSQLScript(self, sql_script_path):
        """
        :param sql_script_path: path to SQL Script (str)
        Execute sql script file
        """
        sql_file = open(sql_script_path, mode='r')
        sql_script = sql_file.read()
        # print(SQLScript)
        conn = self.create_connection()
        try:
            cur = conn.cursor()
            cur.executescript(sql_script)
        except Error as e:
            print(e)
        Database.close_connection(conn)


class SQLQuery(Database):
    """
    class for executing SQL query as object
    """
    def __init__(self, query, db_file="GPDB.db"):
        """
        :param query: query to be executed (str)
        :param db_file: path to sqlite DB file, default GPDB.db (str)
        :return:
        placeholder should be implemented using the Named Method
        You aren't able to use placeholders for column or table names. 
        sql_ = "SELECT * FROM gw_assay WHERE point_id = :id AND analyte = :a AND sampling_date = :d"
        parameters_ = {"id": {point_id}, "a": {analyte}, "d": {sampling_date}}
        OR
        sql_ = "SELECT * FROM gw_assay WHERE point_id = ? AND analyte = ? AND sampling_date = ?"
        par_ = (point_id, analyte, sampling_date)
        """
        Database.__init__(self, db_file)
        self.query = query

    def executeFetchAll(self, decrypter=None, parameters={}, ) -> object:
        """
        :param parameters: dictionary of parameters for the query
        :param decrypter: if an encryption object is available due to successful login it will be used to decrypt result
        :return: a list of tuples for the result array 
        execute the query using the parameters and return the array
        references: https://blog.finxter.com/sqlite-python-placeholder-four-methods-for-sql-statements
        """
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(self.query, parameters)
        result = cur.fetchall()
        Database.close_connection(conn)
        if isinstance(decrypter, EncryptionHelper):
            decrypted_result = list()
            for row in result:
                current_row = list()
                for cell in row:
                    if isinstance(cell, bytes):
                        current_row.append(decrypter.decryptMessage(cell))
                    else:
                        current_row.append(cell)
                decrypted_result.append(current_row)
            return decrypted_result
        
        return result

    def executeCommit(self, parameters={}):
        """
        :param parameters: dictionary of parameters for the query
        :return: a list of list for the result array 
        execute and Commit Insert, Update and Delete query using the parameters and return the last row updated ID
        references: https://www.sqlitetutorial.net/sqlite-python/insert/ 
        """
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(self.query, parameters)
        conn.commit()
        result = cur.lastrowid
        Database.close_connection(conn)
        return result   


if __name__ == '__main__':
    #refresh and create new DB
    #if you have anything that you want to stay permanently edit and insert using sql script
    DB = Database("GPDB.db")
    DB.executeSQLScript("GPDB.sql")

    #testing for query type
    # Q2 = SQLQuery("DELETE FROM UserGroup WHERE UserType = (:type)")
    # result = Q2.executeCommit({"test": "testing", "type": "changed"})
    # Q = SQLQuery("SELECT * FROM UserGroup")
    # result = Q.executeFetchAll()
    # print(result)

    # # testng for storing encrypted value and decrypting it
    Q = SQLQuery("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    EH = EncryptionHelper()
    # noinspection PyTypeChecker
    result = Q.executeCommit(("G01",
                            "testGP", 
                            PasswordHelper.hashPW("testGPPW"),
                            EH.encryptToBits("1991-01-04"),
                            EH.encryptToBits("testGPFitstName"),
                            EH.encryptToBits("testGPLastName"),
                            EH.encryptToBits("0123450233"),
                            EH.encryptToBits("testGPHome Address, test Road"),
                            EH.encryptToBits("A1 7RT"),
                            "GP",
                            "F"))
    # noinspection PyTypeChecker
    result = Q.executeCommit(("1929282829",
                            "testPatient", 
                            PasswordHelper.hashPW("tPPW"),
                            EH.encryptToBits("1982-02-03"),
                            EH.encryptToBits("testPatientFitstName"),
                            EH.encryptToBits("testPatientLastName"),
                            EH.encryptToBits("2929192821"),
                            EH.encryptToBits("testPatientHome Address, test Road"),
                            EH.encryptToBits("A0 5QS"),
                            "Patient",
                            "F"))
    # noinspection PyTypeChecker
    result = Q.executeCommit(("2929282822",
                            "testPatient2", 
                            PasswordHelper.hashPW("tPPW2"),
                            EH.encryptToBits("1984-02-03"),
                            EH.encryptToBits("testPatient2FitstName"),
                            EH.encryptToBits("testPatient2LastName"),
                            EH.encryptToBits("1929292823"),
                            EH.encryptToBits("testPatient2Home Address, test Road"),
                            EH.encryptToBits("B0 5QK"),
                            "Patient",
                            "F"))
    # Q2 = SQLQuery("SELECT * FROM Users")
    # result = Q2.executeFetchAll()
    # print(result)
    # for i in range(3,8):
    #     print(EH.decryptMessage(result[0][i]))
    pass

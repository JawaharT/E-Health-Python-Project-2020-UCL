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
from Encryption import EncryptionHelper
from Encryption import PasswordHelper


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
    # example GP user
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

    result = Q.executeCommit(("G02",
                              "testGP2",
                              PasswordHelper.hashPW("testGPPW02"),
                              EH.encryptToBits("1993-01-05"),
                              EH.encryptToBits("testGP02FitstName"),
                              EH.encryptToBits("testGP02LastName"),
                              EH.encryptToBits("0123432100"),
                              EH.encryptToBits("testGPHome Address, test Road"),
                              EH.encryptToBits("A3 7BA"),
                              "GP",
                              "F"))

    result = Q.executeCommit(("G03",
                              "testGP3",
                              PasswordHelper.hashPW("testGPPW03"),
                              EH.encryptToBits("1989-04-04"),
                              EH.encryptToBits("testGP03FitstName"),
                              EH.encryptToBits("testGP03LastName"),
                              EH.encryptToBits("0129870233"),
                              EH.encryptToBits("testGPHome Address, test Road"),
                              EH.encryptToBits("A5 8DT"),
                              "GP",
                              "F"))
    # example patient user
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

    result = Q.executeCommit(("3334567878",
                              "testPatient3",
                              PasswordHelper.hashPW("tPPW3"),
                              EH.encryptToBits("1984-02-03"),
                              EH.encryptToBits("testPatient3FitstName"),
                              EH.encryptToBits("testPatient3LastName"),
                              EH.encryptToBits("1929292823"),
                              EH.encryptToBits("testPatient3Home Address, test Road"),
                              EH.encryptToBits("B0 5QK"),
                              "Patient",
                              "F"))

    # EH = encryptionHelper()
    # example admin user
    result = Q.executeCommit(("AD1",
                            "testAdmin124",
                            PasswordHelper.hashPW("testAdmin"),
                            EH.encryptToBits("1991-01-04"),
                            EH.encryptToBits("testAdminFirstName"),
                            EH.encryptToBits("testAdminLastName"),
                            EH.encryptToBits("0123450233"),
                            EH.encryptToBits("testAdminHome Address, test Road"),
                            EH.encryptToBits("A1 7RT"),
                            "Admin",
                            "F"))

    result = Q.executeCommit(("AD2",
                              "testAdmin2",
                              PasswordHelper.hashPW("testAdmin2"),
                              EH.encryptToBits("1991-10-08"),
                              EH.encryptToBits("testAdmin02FirstName"),
                              EH.encryptToBits("testAdmin02LastName"),
                              EH.encryptToBits("0123457890"),
                              EH.encryptToBits("testAdmin02Home Address, test Road"),
                              EH.encryptToBits("A1 8BL"),
                              "Admin",
                              "F"))

    result = Q.executeCommit(("AD3",
                              "testAdmin3",
                              PasswordHelper.hashPW("testAdmin3"),
                              EH.encryptToBits("1981-01-04"),
                              EH.encryptToBits("testAdmin03FirstName"),
                              EH.encryptToBits("testAdmin03LastName"),
                              EH.encryptToBits("0123454567"),
                              EH.encryptToBits("testAdmin03Home Address, test Road"),
                              EH.encryptToBits("A1 7RT"),
                              "Admin",
                              "F"))

    result = Q.executeCommit(("AD4",
                              "testAdmin4",
                              PasswordHelper.hashPW("testAdmin4"),
                              EH.encryptToBits("1991-01-04"),
                              EH.encryptToBits("testAdmin04FitstName"),
                              EH.encryptToBits("testAdmin04LastName"),
                              EH.encryptToBits("0123450281"),
                              EH.encryptToBits("test Admin Home Address, test Road"),
                              EH.encryptToBits("AD4 7RT"),
                              "Admin",
                              "F"))


    Q2 = SQLQuery(" INSERT INTO visit VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ")
    EH = EncryptionHelper()
    result = Q2.executeCommit(("1",
                               "1929282829",
                               "G01",
                               "2020-12-25 11:00:00",
                               "fever",
                               "T",
                               "F",
                               "cold, eat some Vitamin C, drink a lot of water and take a lot of rest",
                               "No medicine",
                               "5",
                               ))

    result = Q2.executeCommit(("2",
                               "2929282822",
                               "G02",
                               "2020-12-25 14:00:00",
                               "stomachache",
                               "T",
                               "F",
                               "Gastric cardia, Aspirin Tablet",
                               "None",
                               "4",
                               ))

    result = Q2.executeCommit(("3",
                               "3334567878",
                               "G03",
                               "2020-12-25 14:00:00",
                               "fever",
                               "T",
                               "F",
                               "pneumonia, receive the treatment of intravenous drip in the hospital",
                               "must use Sodium Chloride Injection",
                               "5",
                               ))

    Q3 = SQLQuery("INSERT INTO GP VALUES (?, ?, ?, ?, ?, ?, ?)")
    EH = EncryptionHelper()
    result = Q3.executeCommit(("G01",
                               "F",
                               EH.encryptToBits("test G01 Clinic Address"),
                               EH.encryptToBits("B2 1CH"),
                               "Pediatrics",
                               "Hi,I am G01. I am good at getting along with the children",
                               "5"))

    result = Q3.executeCommit(("G02",
                               "M",
                               EH.encryptToBits("test G02 Clinic Address"),
                               EH.encryptToBits("B2 1CH"),
                               "Orthopedics",
                               "Hi,I am G02. Strong and gentle.",
                               "4"))

    result = Q3.executeCommit(("G03",
                               "M",
                               EH.encryptToBits("test G03 Clinic Address"),
                               EH.encryptToBits("A2 1KL"),
                               "Cardiology",
                               "Hi,I am G03. Take me to your heart",
                               "4"))

    Q4 = SQLQuery("INSERT INTO Patient VALUES (?, ?, ?, ?)")
    EH = EncryptionHelper()
    result = Q4.executeCommit(("1929282829",
                               "F",
                               "I am an accountant",
                               "penicillin allergy"))

    result = Q4.executeCommit(("2929282822",
                               "M",
                               "I am a basketball player",
                               "gluten intolerance"))

    result = Q4.executeCommit(("3334567878",
                               "M",
                               "I am a sales manager",
                               "diabetes"))

    Q5 = SQLQuery("INSERT INTO prescription VALUES (?, ?, ?, ?)")
    EH = EncryptionHelper()
    result = Q5.executeCommit(("1",
                               "Vitamin C",
                               "60 pills",
                               "take 1 or 2 pills after meals "))

    result = Q5.executeCommit(("2",
                               "Aspirin",
                               "6 capsules * 3",
                               "take 0ne capsule after breakast and dinner"))

    result = Q5.executeCommit(("3",
                               "IV ",
                               "500ml *2bottles* 3days",
                               "following 3 days in hospital"))

    # Q = SQLQuery("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    # EH = EncryptionHelper()
    # # noinspection PyTypeChecker
    #
    # Q2 = SQLQuery("SELECT * FROM Users")
    # result = Q2.executeFetchAll()
    # print(result)
    # for i in range(3,8):
    #     print(EH.decryptMessage(result[0][i]))
    pass

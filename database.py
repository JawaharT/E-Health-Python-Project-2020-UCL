import sqlite3
from sqlite3 import Error

from encryption import EncryptionHelper, PasswordHelper


class Database:
    """
    Class for establishing and managing the database connection
    """
    def __init__(self, db_file="GPDB.db"):
        """
        :param str db_file: Path to sqlite .db file, default = GPDB.db
        """
        self.db_file = db_file

    def create_connection(self) -> bool:
        """
        Create a connection to the database
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
            return False
        else:
            return True

    def close_connection(self) -> bool:
        """
        Close an open connection to the database
        """
        if self.conn:
            self.conn.close()
            return True
        else:
            return False


class SQLQuery(Database):
    """
    Class representing an SQL query as an object
    """
    def __init__(self, query):
        """
        :param str query: Query to be executed
        placeholder should be implemented using the Named Method
        You aren't able to use placeholders for column or table names. 
        sql_ = "SELECT * FROM gw_assay WHERE point_id = :id AND analyte = :a AND sampling_date = :d"
        parameters_ = {"id": {point_id}, "a": {analyte}, "d": {sampling_date}}
        OR
        sql_ = "SELECT * FROM gw_assay WHERE point_id = ? AND analyte = ? AND sampling_date = ?"
        par_ = (point_id, analyte, sampling_date)
        """
        super().__init__()
        self.query = query

    def fetch_all(self, decrypter=None, parameters=tuple()) -> list:
        """
        Method to execute the query using the parameters and return a resulting array
        :param tuple parameters: Parameters for the query
        :param decrypter: Object used for decrypting the results
        :return: result array
        references: https://blog.finxter.com/sqlite-python-placeholder-four-methods-for-sql-statements
        """
        if self.create_connection():
            cur = self.conn.cursor()
            self.execute_query(cur, parameters)
            result = cur.fetchall()
            self.close_connection()
            if isinstance(decrypter, EncryptionHelper):
                decrypted_result = list()
                for row in result:
                    current_row = list()
                    for cell in row:
                        if isinstance(cell, bytes):
                            current_row.append(decrypter.decrypt_message(cell))
                        else:
                            current_row.append(cell)
                    decrypted_result.append(current_row)
                return decrypted_result
            return result
        else:
            return []

    def commit(self, parameters=tuple(), multiple_queries=False) -> list:
        """
        :param tuple parameters: Parameters for the query
        :param bool multiple_queries: set true if executing a multi-statement query.
        :return: a list of list for the result array 
        execute and Commit Insert, Update and Delete query using the parameters and return the last row updated ID
        references: https://www.sqlitetutorial.net/sqlite-python/insert/ 
        """
        if self.create_connection():
            cur = self.conn.cursor()
            if not multiple_queries:
                self.execute_query(cur, parameters)
            else:
                self.execute_multiple_query(cur)
            self.conn.commit()
            result = cur.lastrowid
            self.close_connection()
            return result
        else:
            return []

    def execute_query(self, cursor, parameters):
        """
        :param cursor: connection to the database
        :param tuple parameters: Parameters for the query
        """
        try:
            cursor.execute(self.query, parameters)
        except sqlite3.DatabaseError as e:
            print("Database disk image is malformed.", e)
            from iohandler import Parser
            Parser.user_quit()

    def execute_multiple_query(self, cursor):
        try:
            cursor.executescript(self.query)
        except sqlite3.DatabaseError as e:
            print("Database disk image is malformed.", e)
            from iohandler import Parser
            Parser.user_quit()


if __name__ == '__main__':
    # refresh and create new DB
    # if you have anything that you want to stay permanently edit and insert using sql script
    DB = Database("GPDB.db")
    DB.executeSQLScript("GPDB.sql")

    # testing for query type
    # Q2 = SQLQuery("DELETE FROM UserGroup WHERE UserType = (:type)")
    # result = Q2.executeCommit({"test": "testing", "type": "changed"})
    # Q = SQLQuery("SELECT * FROM UserGroup")
    # result = Q.executeFetchAll()
    # print(result)

    # # testng for storing encrypted value and decrypting it
    Q = SQLQuery("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    EH = EncryptionHelper()
    # example GP user
    Q.commit(("G01",
              "testGP",
              PasswordHelper.hash_pw("testGPPW"),
              EH.encrypt_to_bits("1991-01-04"),
              EH.encrypt_to_bits("testGPFitstName"),
              EH.encrypt_to_bits("testGPLastName"),
              EH.encrypt_to_bits("0123450233"),
              EH.encrypt_to_bits("testGPHome Address, test Road"),
              EH.encrypt_to_bits("A1 7RT"),
              "GP",
              "F"))

    Q.commit(("G02",
              "testGP2",
              PasswordHelper.hash_pw("testGPPW02"),
              EH.encrypt_to_bits("1993-01-05"),
              EH.encrypt_to_bits("testGP02FitstName"),
              EH.encrypt_to_bits("testGP02LastName"),
              EH.encrypt_to_bits("0123432100"),
              EH.encrypt_to_bits("testGPHome Address, test Road"),
              EH.encrypt_to_bits("A3 7BA"),
              "GP",
              "F"))

    Q.commit(("G03",
              "testGP3",
              PasswordHelper.hash_pw("testGPPW03"),
              EH.encrypt_to_bits("1989-04-04"),
              EH.encrypt_to_bits("testGP03FitstName"),
              EH.encrypt_to_bits("testGP03LastName"),
              EH.encrypt_to_bits("0129870233"),
              EH.encrypt_to_bits("testGPHome Address, test Road"),
              EH.encrypt_to_bits("A5 8DT"),
              "GP",
              "F"))
    # example patient user
    Q.commit(("1929282829",
              "testPatient",
              PasswordHelper.hash_pw("tPPW"),
              EH.encrypt_to_bits("1982-02-03"),
              EH.encrypt_to_bits("testPatientFitstName"),
              EH.encrypt_to_bits("testPatientLastName"),
              EH.encrypt_to_bits("2929192821"),
              EH.encrypt_to_bits("testPatientHome Address, test Road"),
              EH.encrypt_to_bits("A0 5QS"),
              "Patient",
              "F"))

    Q.commit(("2929282822",
              "testPatient2",
              PasswordHelper.hash_pw("tPPW2"),
              EH.encrypt_to_bits("1984-02-03"),
              EH.encrypt_to_bits("testPatient2FitstName"),
              EH.encrypt_to_bits("testPatient2LastName"),
              EH.encrypt_to_bits("1929292823"),
              EH.encrypt_to_bits("testPatient2Home Address, test Road"),
              EH.encrypt_to_bits("B0 5QK"),
              "Patient",
              "F"))

    Q.commit(("3334567878",
              "testPatient3",
              PasswordHelper.hash_pw("tPPW3"),
              EH.encrypt_to_bits("1984-02-03"),
              EH.encrypt_to_bits("testPatient3FitstName"),
              EH.encrypt_to_bits("testPatient3LastName"),
              EH.encrypt_to_bits("1929292823"),
              EH.encrypt_to_bits("testPatient3Home Address, test Road"),
              EH.encrypt_to_bits("B0 5QK"),
              "Patient",
              "F"))

    # example admin user
    Q.commit(("AD1",
              "testAdmin124",
              PasswordHelper.hash_pw("testAdmin"),
              EH.encrypt_to_bits("1991-01-04"),
              EH.encrypt_to_bits("testAdminFirstName"),
              EH.encrypt_to_bits("testAdminLastName"),
              EH.encrypt_to_bits("0123450233"),
              EH.encrypt_to_bits("testAdminHome Address, test Road"),
              EH.encrypt_to_bits("A1 7RT"),
              "Admin",
              "F"))

    Q.commit(("AD2",
              "testAdmin2",
              PasswordHelper.hash_pw("testAdmin2"),
              EH.encrypt_to_bits("1991-10-08"),
              EH.encrypt_to_bits("testAdmin02FirstName"),
              EH.encrypt_to_bits("testAdmin02LastName"),
              EH.encrypt_to_bits("0123457890"),
              EH.encrypt_to_bits("testAdmin02Home Address, test Road"),
              EH.encrypt_to_bits("A1 8BL"),
              "Admin",
              "F"))

    Q.commit(("AD3",
              "testAdmin3",
              PasswordHelper.hash_pw("testAdmin3"),
              EH.encrypt_to_bits("1981-01-04"),
              EH.encrypt_to_bits("testAdmin03FirstName"),
              EH.encrypt_to_bits("testAdmin03LastName"),
              EH.encrypt_to_bits("0123454567"),
              EH.encrypt_to_bits("testAdmin03Home Address, test Road"),
              EH.encrypt_to_bits("A1 7RT"),
              "Admin",
              "F"))

    Q.commit(("AD4",
              "testAdmin4",
              PasswordHelper.hash_pw("testAdmin4"),
              EH.encrypt_to_bits("1991-01-04"),
              EH.encrypt_to_bits("testAdmin04FitstName"),
              EH.encrypt_to_bits("testAdmin04LastName"),
              EH.encrypt_to_bits("0123450281"),
              EH.encrypt_to_bits("test Admin Home Address, test Road"),
              EH.encrypt_to_bits("AD4 7RT"),
              "Admin",
              "F"))

    Q2 = SQLQuery(" INSERT INTO visit VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ")
    Q2.commit(("1",
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

    Q2.commit(("2",
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

    Q2.commit(("3",
               "1929282829",
               "G03",
               "2020-12-25 14:00:00",
               "fever",
               "T",
               "F",
               "pneumonia, receive the treatment of intravenous drip in the hospital",
               "must use Sodium Chloride Injection",
               "5",
               ))
    Q2.commit(("4",
               "1929282829",
               "G03",
               "2020-12-25 14:00:00",
               "fever",
               "T",
               "T",
               "pneumonia, receive the treatment of intravenous drip in the hospital",
               "must use Sodium Chloride Injection",
               "5",
               ))
    Q2.commit(("5",
               "3334567878",
               "G03",
               "2020-12-25 14:00:00",
               "fever",
               "T",
               "T",
               "pneumonia, receive the treatment of intravenous drip in the hospital",
               "must use Sodium Chloride Injection",
               "5",
               ))

    Q3 = SQLQuery("INSERT INTO GP VALUES (?, ?, ?, ?, ?, ?, ?)")
    Q3.commit(("G01",
               "F",
               EH.encrypt_to_bits("test G01 Clinic Address"),
               EH.encrypt_to_bits("B2 1CH"),
               "Pediatrics",
               "Hi,I am G01. I am good at getting along with the children",
               "5"))

    Q3.commit(("G02",
               "M",
               EH.encrypt_to_bits("test G02 Clinic Address"),
               EH.encrypt_to_bits("B2 1CH"),
               "Orthopedics",
               "Hi,I am G02. Strong and gentle.",
               "4"))

    Q3.commit(("G03",
               "M",
               EH.encrypt_to_bits("test G03 Clinic Address"),
               EH.encrypt_to_bits("A2 1KL"),
               "Cardiology",
               "Hi,I am G03. Take me to your heart",
               "4"))

    Q4 = SQLQuery("INSERT INTO Patient VALUES (?, ?, ?, ?)")
    Q4.commit(("1929282829",
               "F",
               "I am an accountant",
               "penicillin allergy"))

    Q4.commit(("2929282822",
               "M",
               "I am a basketball player",
               "gluten intolerance"))

    Q4.commit(("3334567878",
               "M",
               "I am a sales manager",
               "diabetes"))

    Q5 = SQLQuery("INSERT INTO prescription VALUES (?, ?, ?, ?)")
    Q5.commit(("1",
               "Vitamin C",
               "60 pills",
               "take 1 or 2 pills after meals "))

    Q5.commit(("2",
               "Aspirin",
               "6 capsules * 3",
               "take 0ne capsule after breakfast and dinner"))

    Q5.commit(("3",
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

import sqlite3
import sys
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

    def recreate_database(self, sql_script_path):
        """
        :param sql_script_path: path to SQL Script (str)
        Execute sqlscript file
        """
        sql_file = open(sql_script_path, mode='r')
        sql_script = sql_file.read()
        self.create_connection()
        EH = EncryptionHelper()
        try:
            cur = self.conn.cursor()
            cur.executescript(sql_script)
            SQLQuery("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                     ).commit(("AD1", "testAdmin", PasswordHelper.hash_pw("testAdmin"), EH.encrypt_to_bits("1991-01-04")
                               , EH.encrypt_to_bits("testAdminFirstName"), EH.encrypt_to_bits("testAdminLastName"),
                               EH.encrypt_to_bits("0123450233"), EH.encrypt_to_bits("testAdminHome Address, test Road"),
                               EH.encrypt_to_bits("A1 7RT"), "Admin", "F", 0))
        except Error as e:
            print(e)
        self.close_connection()


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
    """
    If the file is run, it will attempt to recreate the database using existing schema.
    Only one user will be added - testAdmin
    """
    while True:
        try:
            DB = Database("GPDB.db")
            database_path = input("Enter the name of the SQL script to execute: ")
            DB.recreate_database(database_path)
        except:
            print("Error recreating the database!")
        else:
            sys.quit()

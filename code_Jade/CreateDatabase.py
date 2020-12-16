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
        return conn
        #print(sqlite3.version)
    except Error as e:
        print(e)
    #finally:
    #   if conn:
    #       conn.close()


def executeSQLScript(SQLScriptPath, db_file):
    '''
    file -> None 
    Execute sqlscript file 
    '''
    SQLfile = open(SQLScriptPath, mode='r')
    SQLScript = SQLfile.read()
    #print(SQLScript)
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
        SQLfile.close()


if __name__ == '__main__':
    db_name = "GPDB.db"
    create_connection(db_name)
    executeSQLScript("GPDB.sql", db_name)

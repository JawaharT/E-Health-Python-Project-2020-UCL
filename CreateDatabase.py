import sqlite3


def create_connection(db_file):
    """Create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None"""

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement"""

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def duplicateUsername(cur, table, username):
    """Check if username has been previously used before inserting record into table."""

    cur.execute("SELECT USERNAME FROM {0} WHERE USERNAME = ?".format(table), (username,))
    if cur.fetchone() is None:
        return True
    else:
        return False


def createAdmins(conn, admin):
    """Create admins in Admin table."""

    cur = conn.cursor()
    isNotDuplicate = duplicateUsername(cur, "admins", admin[-2])
    if isNotDuplicate:
        sql = '''INSERT INTO admins(first_name, last_name, username, password) VALUES(?,?,?,?)'''
        cur.execute(sql, admin)
        conn.commit()
    cur.close()


def createPatients(conn, patient):
    """Create Patients in Patient table."""

    cur = conn.cursor()
    isNotDuplicate = duplicateUsername(cur, "patients", patient[-2])
    if isNotDuplicate:
        sql = '''INSERT INTO patients(first_name, last_name, username, password) VALUES(?,?,?,?)'''
        cur.execute(sql, patient)
        conn.commit()
    cur.close()


def createGPs(conn, gp):
    """Create GPs in GP table."""

    cur = conn.cursor()
    isNotDuplicate = duplicateUsername(cur, "GPs", gp[-2])
    if isNotDuplicate:
        sql = '''INSERT INTO GPs(first_name, last_name, username, password) VALUES(?,?,?,?)'''
        cur.execute(sql, gp)
        conn.commit()
    cur.close()


def main():
    """Create database with 3 tables and store it inside database.db"""

    database = "database.db"

    sql_create_admins_table = """CREATE TABLE IF NOT EXISTS admins (
                                        admin_id integer PRIMARY KEY,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        username text NOT NULL,
                                        password test NOT NULL); """

    sql_create_patients_table = """CREATE TABLE IF NOT EXISTS patients (
                                    patient_id integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    username text NOT NULL,
                                    password test NOT NULL);"""

    sql_create_gps_table = """CREATE TABLE IF NOT EXISTS GPs (
                                        GP_id integer PRIMARY KEY,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        username text NOT NULL,
                                        password test NOT NULL);"""

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        # Create Admins Table
        create_table(conn, sql_create_admins_table)

        # Create Patients Table
        create_table(conn, sql_create_patients_table)

        # Create GPs Table
        create_table(conn, sql_create_gps_table)

        # Add records to tables
        createAdmins(conn, ("Admin1", "Darwin", "darwinian", "not encrypted"))
        createPatients(conn, ("Patient1", "Patient1 Last name", "Patient 1 username", "not encrypted yet"))
        createGPs(conn, ("GP1", "GP1 Last name", "GP1 username", "not encrypted yet"))
    else:
        print("Cannot create the connection to database.")

    if conn:
        conn.close()
        print("The SQLite connection is closed.")


if __name__ == '__main__':
    main()

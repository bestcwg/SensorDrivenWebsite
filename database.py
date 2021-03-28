""" Database functions for connection with the database """

import sqlite3

__MEASUREMENTS_DB = "db/measurements.db"
__CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS measurements
                    (temp INTEGER NOT NULL,
                    hum INTEGER NOT NULL,
                    pres INTEGER NOT NULL,
                    date TEXT NOT NULL)
"""

def create_database():
    """Creates the database"""
    with sqlite3.connect(
        __MEASUREMENTS_DB, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        cur = conn.cursor()
        cur.execute(__CREATE_SQL)
        conn.commit()

def store_data(temp, hum, pres, time):
    """Storing measurements from m5stick"""
    with sqlite3.connect(
        __MEASUREMENTS_DB, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        cur = conn.cursor()
        data = (temp, hum, pres, time)
        cur.execute("INSERT INTO measurements VALUES(?,?,?,?)", data)
        conn.commit()

def get_all_measurements():
    """ Getting measurements from database

    Returns:
        List: of measurements in the database
    """
    with sqlite3.connect(
        __MEASUREMENTS_DB, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("SELECT * FROM measurements ORDER BY date ASC")
        return cur.fetchall()

def get_from_database(data):
    """ Gets measurents from database, accordingly to the parameter
    
    Returns:
        List: of measurements
    """ 
    choice = {
        'latest' : "SELECT * FROM measurements ORDER BY date DESC",
        'mintemp' : "SELECT date, MIN(temp) FROM measurements",
        'maxtemp' : "SELECT date, MAX(temp) FROM measurements",
        'minhum' : "SELECT date, MIN(hum) FROM measurements",
        'maxhum' : "SELECT date, MAX(hum) FROM measurements",
        'minpres' : "SELECT date, MIN(pres) FROM measurements",
        'maxpres' : "SELECT date, MAX(pres) FROM measurements"
    }[data]
    with sqlite3.connect(
        __MEASUREMENTS_DB, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute(choice)
        return cur.fetchone()

def get_data(offset):
    """ Gets data from database and offset by 20 * offset

    Returns:
        List: of 20 measurements offset by input
    """
    with sqlite3.connect(
        __MEASUREMENTS_DB, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM measurements ORDER BY date ASC LIMIT 20 OFFSET ?", (offset,)
        )
        return cur.fetchall()

def dict_factory(cursor, row):
    dic = {}
    for idx, col in enumerate(cursor.description):
        dic[col[0]] = row[idx]
    return dic

if __name__ != "__main__":
    create_database()

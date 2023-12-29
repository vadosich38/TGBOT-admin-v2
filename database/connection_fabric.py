#TODO документировать

import sqlite3 as sq


def get_db_conn(db_name: str = "../my_db.db") -> sq.Connection:
    conn = sq.connect(database=db_name)

    return conn

import sqlite3 as sq


def get_db_conn(db_name: str = "my_db.db") -> sq.Connection:
    """
    Функция создает и возвращает объект соединения с БД
    :param db_name: имя БД, к которой идет подключение
    :return: объект подключения к БД
    """
    conn = sq.connect(database=db_name)

    return conn

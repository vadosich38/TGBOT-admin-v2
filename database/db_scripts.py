#TODO документировать

import sqlite3 as sq


class DbMethods:
    @staticmethod
    def db_create(conn: sq.Connection) -> None:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY,
                        admin INTEGER NOT NULL,
                        donor_id INTEGER,
                        active INTEGER NOT NULL,
                        last_active TEXT)""")

    @staticmethod
    def add_user(user_id: int,
                 admin: int,
                 donor_id: int,
                 active: int,
                 last_active: str,
                 conn: sq.Connection) -> None:

        cur = conn.cursor()
        cur.execute("""INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?, ?)""",
                    (user_id,
                     admin,
                     donor_id,
                     active,
                     last_active))

    @staticmethod
    def check_user_status(user_id: int, conn: sq.Connection) -> str:
        cur = conn.cursor()

        try:
            res = cur.execute("SELECT admin FROM users WHERE user_id LIKE(?)", (user_id, )).fetchone()[0]
        except TypeError:
            return "no user"

        if res == 1:
            return "admin"
        elif res == 0:
            return "not admin"

    @staticmethod
    def update_to_admin(user_id: int,
                        donor_id: int,
                        conn: sq.Connection) -> None:
        cur = conn.cursor()
        cur.execute("""UPDATE users SET admin = ?, donor_id = ? WHERE user_id LIKE (?)""", (1, donor_id, user_id, ))

    @staticmethod
    def get_users_id(conn: sq.Connection) -> list:
        cur = conn.cursor()

        users_id = cur.execute("""SELECT user_id FROM users""").fetchall()
        return users_id

    @staticmethod
    def update_user_data(conn: sq.Connection, user_id: int, active: int, last_active: str = None) -> None:
        cur = conn.cursor()
        if not last_active:
            cur.execute("""UPDATE users SET active = ? WHERE user_id LIKE(?)""", (active,
                                                                                  user_id, ))
        else:
            cur.execute("""UPDATE users SET active = ?, last_active = ? WHERE user_id LIKE(?)""", (active,
                                                                                                   last_active,
                                                                                                   user_id, ))

    @staticmethod
    def delete_admin(user_id: int, conn: sq.Connection) -> None:
        cur = conn.cursor()

        cur.execute("""UPDATE users SET admin = ? WHERE user_id LIKE(?)""", (0, user_id, ))

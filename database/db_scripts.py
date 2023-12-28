import sqlite3 as sq


async def db_create() -> None:
    with sq.connect("../my_db.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY,
                        admin INTEGER NOT NULL,
                        donor_id INTEGER,
                        active INTEGER NOT NULL,
                        last_active TEXT)""")


async def add_user(user_id: int,
                   admin: int,
                   donor_id: int,
                   active: int,
                   last_active: str) -> None:
    with sq.connect("../my_db.db") as con:
        cur = con.cursor()
        cur.execute("""INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?, ?)""",
                    (user_id,
                     admin,
                     donor_id,
                     active,
                     last_active))


async def check_user_status(user_id: str) -> str:
    with sq.connect("../my_db.db") as con:
        cur = con.cursor()

        try:
            res = cur.execute("SELECT admin FROM users WHERE user_id LIKE(?)", (user_id, )).fetchone()[0]
        except TypeError:
            return "no user"

        if res == 1:
            return "admin"
        elif res == 0:
            return "not admin"


async def update_to_admin(user_id: int,
                          donor_id: int) -> None:
    with sq.connect("../my_db.db") as con:
        cur = con.cursor()
        cur.execute("""UPDATE users SET admin = ?, donor_id = ? WHERE user_id LIKE (?)""", (1, donor_id, user_id, ))


async def get_users_id() -> list:
    with sq.connect("../my_db.db") as con:
        cur = con.cursor()

        users_id = cur.execute("""SELECT user_id FROM users""").fetchall()
        return users_id


async def update_user_data(user_id: int, active: int, last_active: str = None) -> None:
    with sq.connect("../my_db.db") as con:
        cur = con.cursor()
        if not last_active:
            cur.execute("""UPDATE users SET active = ? WHERE user_id LIKE(?)""", (active,
                                                                                  user_id, ))
        else:
            cur.execute("""UPDATE users SET active = ?, last_active = ? WHERE user_id LIKE(?)""", (active,
                                                                                                   last_active,
                                                                                                   user_id, ))


async def delete_admin(user_id: int) -> None:
    with sq.connect("../my_db.db") as con:
        cur = con.cursor()

        cur.execute("""UPDATE users SET admin = ? WHERE user_id LIKE(?)""", (0, user_id, ))


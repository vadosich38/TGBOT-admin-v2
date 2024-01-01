#TODO документировать

import sqlite3 as sq


class DbMethods:
    """
    Класс работы с базой данных
    """
    @staticmethod
    def db_create(conn: sq.Connection) -> None:
        """
        Метод создания базы данных
        :param conn: объект подключения к бд
        :return: None
        """
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
                 active: int,
                 last_active: str,
                 conn: sq.Connection,
                 donor_id: int = 0
                 ) -> None:
        """
        Метод добавления нового пользователя бота в БД
        :param user_id: TELEGRAM ID пользователя
        :param admin: флаг является ли пользователь администратором, 1 - true, 0 - false
        :param donor_id: TELEGRAM ID пользователя-родителя администратора
        :param active: статус пользователя, 1 - активный, 0 - не активный
        :param last_active: дата поселдней активности пользователя (дата добавления пользователя)
        :param conn: объект подключения к БД
        :return: None
        """

        cur = conn.cursor()
        cur.execute("""INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?, ?)""",
                    (user_id,
                     admin,
                     donor_id,
                     active,
                     last_active))

    @staticmethod
    def check_user_status(user_id: int, conn: sq.Connection) -> str:
        """
        Метод првоерки статуса пользователя
        :param user_id: TELEGRAM ID пользователя, которого проверяем
        :param conn: объект подключения к БД
        :return: str (статус пользователя в строковом виде)
        """
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
        """
        Метод назначения пользователя администратором бота
        :param user_id: TELEGRAM ID пользователя, которого назначают админом
        :param donor_id: TELEGRAM ID пользователя-родителя, который назначает пользователя админом
        :param conn: объект подключения к БД
        :return: None
        """
        cur = conn.cursor()
        cur.execute("""UPDATE users SET admin = ?, donor_id = ? WHERE user_id LIKE (?)""", (1, donor_id, user_id, ))

    @staticmethod
    def get_users_id(conn: sq.Connection) -> list:
        """
        Метод получения списка всех пользователей бота
        :param conn: объект подключения к БД
        :return: (list) список всех пользователей бота
        """
        cur = conn.cursor()

        users_id = cur.execute("""SELECT user_id FROM users""").fetchall()
        return users_id

    @staticmethod
    def update_user_data(conn: sq.Connection, user_id: int, active: int, last_active: str = None) -> None:
        """
        Метод обновления данных о пользователе в БД
        :param conn: объект подключения к БД
        :param user_id: TELEGRAM ID пользователя, информация о котором обновляется
        :param active: статус активности пользователя, 1 - активный, 0 - не активный
        :param last_active: дата полследней активности пользователя
        :return: None
        """
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
        """
        Метод удаления администратора (разжаловать администратора до пользователя)
        :param user_id: TELEGRAM ID пользователя, которого нужно разжаловать до пользователя
        :param conn: объект подключения к БД
        :return: None
        """
        cur = conn.cursor()

        cur.execute("""UPDATE users SET admin = ? WHERE user_id LIKE(?)""", (0, user_id, ))

import psycopg2 as dbapi2
from xapian import DatabaseError

class User:
    def __init__(self, app):
        self.app = app

    def List_Users(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """ SELECT * FROM USERS ORDER BY USER_ID"""
            cursor.execute(query)
            users = cursor.fetchall()
            return users

    def Add_Users(self, username, name, surname, email, password):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """INSERT INTO USERS (USERNAME, NAME, SURNAME, EMAIL, PASSWORD,
                FOLLOWERCOUNT)
                VALUES ('"""+ username  +"""', '"""+ name +"""', '"""+ surname +"""', '"""+ email +"""', '"""+ password +"""', 0)"""
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

    def Delete_Users(self, pick):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "SELECT USER_ID FROM USERS WHERE USERNAME = '" + pick + "'"
                cursor.execute(query)
                tmp = cursor.fetchone()
                if tmp is not None:
                    query = "DELETE FROM USERS WHERE USERNAME = '" + pick + "'"
                    cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

    def Update_Users(self, pick, username, name, surname, email, password):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "SELECT USER_ID FROM USERS WHERE USERNAME = '" + pick + "'"
                cursor.execute(query)
                tmp = cursor.fetchone()
                if tmp is not None:
                    query = """UPDATE USERS
                    SET USERNAME = '"""+ username +"""', NAME = '"""+ name +"""',
                    SURNAME = '"""+ surname +"""', EMAIL = '"""+ email +"""',
                    PASSWORD = '"""+ password +"""'
                    WHERE USERNAME = '""" + pick +"""'"""
                    cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

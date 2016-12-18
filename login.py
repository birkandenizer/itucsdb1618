import psycopg2 as dbapi2

class Login:
    def __init__(self, app):
        self.app = app

    def Get_UserID(self, username, password):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """SELECT PASSWORD FROM USERS WHERE USERNAME = %s """
                cursor.execute(query, (username,))
                passw = cursor.fetchone()
                if password != passw[0]:
                    return -1
                query = """SELECT USER_ID FROM USERS WHERE USERNAME = %s """
                cursor.execute(query, (username,))
                userid = cursor.fetchone()
                return userid
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()
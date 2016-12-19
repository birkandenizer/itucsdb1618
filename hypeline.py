import psycopg2 as dbapi2

class Hypeline:
    def __init__(self, app):
        self.app = app

    def List_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """SELECT USERNAME, TEXT, TOPIC, DATE FROM HYPES INNER JOIN USERS
                        ON USERS.USER_ID = HYPES.USER_ID"""
                cursor.execute(query)
                hypes = cursor.fetchall()
                return hypes
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

    def List_Hypes_User(self, username):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """SELECT USERNAME, TEXT, TOPIC, DATE FROM HYPES INNER JOIN USERS
                        ON USERS.USER_ID = HYPES.USER_ID WHERE USERS.USERNAME = %s"""
                cursor.execute(query, (username,))
                hypes = cursor.fetchall()
                return hypes
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()
                
    def List_Hypes_Hypeline(self, username):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """SELECT USERNAME, TEXT, TOPIC, HYPES.DATE FROM USERS INNER JOIN FOLLOWER
                        ON USERS.USER_ID = FOLLOWER.FOLLOWER_ID INNER JOIN
                        HYPES ON HYPES.USER_ID = FOLLOWER.FOLLOWER_ID
                        WHERE FOLLOWER.PERSON_ID = %s ORDER BY DATE DESC"""
                cursor.execute(query, (username,))
                hypes = cursor.fetchall()
                return hypes
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()


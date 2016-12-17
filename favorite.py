import psycopg2 as dbapi2
import datetime

class Favorite:
    def __init__(self, app):
        self.app = app

    def initialize_Favorite(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(""" CREATE TABLE IF NOT EXISTS FAVORITES(
                ID SERIAL PRIMARY KEY,
                HYPE_ID INTEGER NOT NULL REFERENCES HYPES (HYPE_ID) ON DELETE CASCADE,
                USER_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                DATE DATE NOT NULL,
                RATE INTEGER NOT NULL,
                UNIQUE(HYPE_ID,USER_ID)
                )""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def drop_Favorite(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """DROP TABLE IF EXISTS FAVORITES"""
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def List_Favorites(self, user_ids):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM FAVORITES WHERE USER_ID = %s ORDER BY DATE ASC"""
             cursor.execute(query,(user_ids))
             favorites = cursor.fetchall()
             return favorites

    def List_FavoritesID(self, favorite_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM FAVORITES WHERE ID = %s ORDER BY DATE ASC"""
             cursor.execute(query,(favorite_id))
             favorites = cursor.fetchall()
             return favorites

    def Delete_Favorite(self, favorite_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM FAVORITES WHERE (ID = %s)"""
                cursor.execute(query, (favorite_id,))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Add_Favorite(self, user_ids, hype_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                rate = 1
                cursor = connection.cursor()
                query =  """INSERT INTO FAVORITES(HYPE_ID, USER_ID, DATE, RATE) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (hype_id, user_ids, date, rate))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Update_Favorite(self, favorite_id, rate):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """UPDATE FAVORITES
                             SET RATE = %s
                             WHERE (ID = %s)"""
                cursor.execute(query, (rate, favorite_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
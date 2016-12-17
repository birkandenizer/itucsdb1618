import psycopg2 as dbapi2
import datetime

class dislike:
    def __init__(self, app):
        self.app = app

    def initialize_table(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(""" CREATE TABLE IF NOT EXISTS DISLIKES(
                ID SERIAL PRIMARY KEY,
                HYPE_ID INTEGER NOT NULL REFERENCES HYPES (HYPE_ID) ON DELETE CASCADE,
                USER_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                DATE DATE NOT NULL,
                REASON VARCHAR(50),
                UNIQUE(HYPE_ID,USER_ID)
                )""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def List_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM HYPES ORDER BY HYPES"""
             cursor.execute(query)
             dislike_hypes = cursor.fetchall()
             return dislike_hypes

    def select_dislikes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM DISLIKES """
             cursor.execute(query)
             users_dislike = cursor.fetchall()
             return users_dislike

    def delete_dislike(self, hype_id, user_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM DISLIKES WHERE HYPE_ID = %s AND USER_ID = %s"""
                cursor.execute(query, (hype_id, user_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def add_dislike(self, user_id, hype_id, reason):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                cursor = connection.cursor()
                query =  """INSERT INTO DISLIKES(HYPE_ID, USER_ID, DATE, REASON) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (user_id, hype_id, date, reason))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()


    def update_reason(self, hype_id, user_id, reason):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """UPDATE DISLIKES SET REASON = %s WHERE HYPE_ID=%s AND USER_ID=%s"""
                cursor.execute(query, (reason, hype_id, user_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def select_users(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM USERS """
             cursor.execute(query)
             sportuser = cursor.fetchall()
             return sportuser
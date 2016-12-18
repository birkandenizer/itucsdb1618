import psycopg2 as dbapi2
import datetime

class block:
    def __init__(self, app):
        self.app = app
        
    def initialize_table(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(""" CREATE TABLE IF NOT EXISTS BLOCKED(
                PERSON_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                BLOCK_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                REASON VARCHAR(50),
                DATE DATE NOT NULL,
                PRIMARY KEY(PERSON_ID,BLOCK_ID)
                )""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def show_blocked(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM BLOCKED """
             cursor.execute(query)
             sportpage = cursor.fetchall()
             return sportpage


    def select_block(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM BLOCKED"""
             cursor.execute(query)
             sportpage = cursor.fetchall()
             return sportpage


    def add_block(self, person_id, block_id, reason):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                cursor = connection.cursor()
                query =  """INSERT INTO BLOCKED(PERSON_ID, BLOCK_ID, REASON, DATE) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (person_id, block_id, reason, date))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()


    def delete_block(self, person_id, block_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM BLOCKED WHERE PERSON_ID = %s AND BLOCK_ID = %s"""
                cursor.execute(query, (person_id, block_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def update_reason(self, person_id, block_id, reason):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """UPDATE BLOCKED SET REASON = %s WHERE PERSON_ID=%s AND BLOCK_ID=%s"""
                cursor.execute(query, (reason, person_id, block_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()





    def select_users(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM BLOCKED """
             cursor.execute(query)
             sportuser2 = cursor.fetchall()
             return sportuser2




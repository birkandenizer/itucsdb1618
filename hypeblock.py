import psycopg2 as dbapi2
import datetime

class Hypeblock:
    def __init__(self, app):
        self.app = app

    def initialize_table(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS HYPEBLOCKS (
                ID          SERIAL PRIMARY KEY NOT NULL,
                USER_ID     INT NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                HYPE_ID     INT NOT NULL REFERENCES HYPES (HYPE_ID) ON DELETE CASCADE,
                DATE        DATE NOT NULL,
                REASON      VARCHAR(50),
                PERSONAL    BOOLEAN NOT NULL,
                UNIQUE(HYPE_ID,USER_ID)
                )""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

    def drop_table(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""DROP TABLE IF EXISTS HYPEBLOCKS""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

    def List_BlockedHypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM HYPEBLOCKS"""
             cursor.execute(query)
             blocks = cursor.fetchall()
             return blocks

    def Add_BlockedHypes(self, user_id, hype_id, reason, personal):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                cursor = connection.cursor()
                query =  """INSERT INTO HYPEBLOCKS(USER_ID, HYPE_ID, DATE, REASON, PERSONAL) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (user_id, hype_id, date, reason, personal))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Delete_BlockedHypes(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM HYPEBLOCKS WHERE (ID = %s)"""
                cursor.execute(query, (id,))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Update_BlockedHypes(self, id, hype_id, reason, personal):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """UPDATE HYPEBLOCKS SET REASON = %s, HYPE_ID = %s, PERSONAL = %s WHERE ID = %s"""
                cursor.execute(query, (reason, hype_id, personal, id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

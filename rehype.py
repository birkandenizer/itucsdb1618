import psycopg2 as dbapi2
import datetime

class Rehype:
    def __init__(self, app):
        self.app = app

    def initialize_Rehype(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(""" CREATE TABLE IF NOT EXISTS REHYPES(
                HYPE_ID INTEGER NOT NULL REFERENCES HYPES (HYPE_ID) ON DELETE CASCADE,
                USER_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                COMMENT VARCHAR(200),
                DATE DATE NOT NULL,
                PRIMARY KEY (HYPE_ID, USER_ID)
                )""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def drop_Rehype(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """DROP TABLE IF EXISTS REHYPES"""
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def List_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM HYPES WHERE TOPIC = 'Music' ORDER BY DATE ASC"""
             cursor.execute(query)
             hypespage = cursor.fetchall()
             return hypespage
            
    def List_News_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM HYPES WHERE TOPIC = 'News' ORDER BY DATE ASC"""
             cursor.execute(query)
             newsHypespage = cursor.fetchall()
             return newsHypespage

    def List_Tech_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM HYPES WHERE TOPIC = 'Technology' ORDER BY DATE ASC"""
             cursor.execute(query)
             TechHypespage = cursor.fetchall()
             return TechHypespage

    def List_Events_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM HYPES WHERE TOPIC = 'Events' ORDER BY DATE ASC"""
             cursor.execute(query)
             EventsHypespage = cursor.fetchall()
             return EventsHypespage

    def List_Rehypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM REHYPES ORDER BY DATE ASC"""
             cursor.execute(query)
             rehypespage = cursor.fetchall()
             return rehypespage
            
    def List_RehypesUser(self, user_ids):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             user_ids = str(user_ids)
             cursor = connection.cursor()
             query = """ SELECT * FROM REHYPES WHERE USER_ID = %s ORDER BY DATE ASC"""
             cursor.execute(query,(user_ids))
             rehypespage = cursor.fetchall()
             return rehypespage

    def Add_Rehype(self, user_id, hype_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                comment = "Please write your comment to this rehype!"
                cursor = connection.cursor()
                query =  """INSERT INTO REHYPES(HYPE_ID, USER_ID, COMMENT, DATE) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (hype_id, user_id, comment, date))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Delete_Rehype(self, user_id, hype_ids):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """ SELECT HYPE_ID FROM REHYPES WHERE USER_ID = %s"""
                cursor.execute(query,(user_id))
                hype_id = cursor.fetchall()
                cursor = connection.cursor()
                query =  """DELETE FROM REHYPES WHERE (USER_ID = %s) AND (HYPE_ID = %s)"""
                cursor.execute(query, (user_id, hype_ids,))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
                return hype_ids
            finally:
               connection.commit()
               return hype_ids

    def Update_Rehype(self, old_user_id, hype_id, comment, user_ids):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                cursor = connection.cursor()
                query =  """UPDATE REHYPES
                             SET COMMENT = %s,
                             USER_ID = %s
                             WHERE (USER_ID = %s) AND (HYPE_ID = %s)"""
                cursor.execute(query, (comment, user_ids, old_user_id, hype_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def List_Users(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM USERS """
             cursor.execute(query)
             hypespageUsername = cursor.fetchall()
             return hypespageUsername

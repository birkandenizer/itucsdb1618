import psycopg2 as dbapi2
import datetime

class Rehype:
    def __init__(self, app):
        self.app = app

    def List_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM HYPES WHERE TOPIC = 'Music' ORDER BY DATE ASC"""
             cursor.execute(query)
             hypespage = cursor.fetchall()
             return hypespage

    def List_Rehypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM REHYPES ORDER BY DATE ASC"""
             cursor.execute(query)
             rehypespage = cursor.fetchall()
             return rehypespage

    #def Get_Name(self, user_id):
        #with dbapi2.connect(self.app.config['dsn']) as connection:
             #cursor = connection.cursor()
             #query = """ SELECT username FROM USERS WHERE USER_ID = %s """
             #cursor.execute(query, [user_id])
             #users = cursor.fetchall()
             #return users

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

    def Delete_Rehype(self, user_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM REHYPES WHERE (USER_ID = %s)"""
                cursor.execute(query, (user_id,))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Update_Rehype(self, hype_id, comment):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                cursor = connection.cursor()
                query =  """UPDATE REHYPES SET COMMENT = %s WHERE HYPE_ID = %s"""
                cursor.execute(query, (comment, hype_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
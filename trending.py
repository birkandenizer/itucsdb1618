import psycopg2 as dbapi2
import datetime

class Trending:
    def __init__(self, app):
        self.app = app

    def initialize_Trending(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(""" CREATE TABLE IF NOT EXISTS TRENDING(
                ID SERIAL PRIMARY KEY,
                HYPE_ID INTEGER NOT NULL REFERENCES HYPES (HYPE_ID) ON DELETE CASCADE,
                TAG VARCHAR(20) NOT NULL,
                DATE DATE NOT NULL,
                COUNT INTEGER NOT NULL,
                UNIQUE(HYPE_ID)
                )""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def List_Trending(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM TRENDING ORDER BY COUNT DESC"""
             cursor.execute(query)
             trending = cursor.fetchall()
             return trending

    def List_Trending_Hypes(self, hype_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM HYPES WHERE HYPE_ID = %s ORDER BY DATE ASC"""
             cursor.execute(query,(hype_id))
             hypespage = cursor.fetchall()
             return hypespage

    def Decision_Add(self, hype_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT COUNT(*) FROM REHYPES WHERE HYPE_ID = %s"""
             cursor.execute(query,(hype_id))
             rehype_count = cursor.fetchall()
             cursor = connection.cursor()
             query = """ SELECT COUNT(*) FROM TRENDING WHERE HYPE_ID = %s"""
             cursor.execute(query,(hype_id))
             trending_count = cursor.fetchall()
             query = """ SELECT TEXT FROM HYPES WHERE HYPE_ID = %s"""
             cursor.execute(query,(hype_id))
             text = cursor.fetchall()
             word = text[0][0].split()[0]
             if rehype_count[0][0] == 3 :
                 if trending_count[0][0] == 0:
                     element = [hype_id, rehype_count[0][0], word]
                     return element
             else :
                 return 0

    def Decision_Update_Add(self, hype_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             hype_id = str(hype_id)
             cursor = connection.cursor()
             query = """ SELECT COUNT(*) FROM REHYPES WHERE HYPE_ID = %s"""
             cursor.execute(query,(hype_id))
             rehype_count = cursor.fetchall()
             cursor = connection.cursor()
             query = """ SELECT COUNT(*) FROM TRENDING WHERE HYPE_ID = %s"""
             cursor.execute(query,(hype_id))
             trending_count = cursor.fetchall()
             if rehype_count[0][0] > 3 :
                 if trending_count[0][0] > 0:
                     return True

    def Decision_Update_Del(self, hype_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             hype_id = str(hype_id)
             cursor = connection.cursor()
             query = """ SELECT COUNT(*) FROM REHYPES WHERE HYPE_ID = %s"""
             cursor.execute(query,(hype_id))
             rehype_count = cursor.fetchall()
             cursor = connection.cursor()
             query = """ SELECT COUNT(*) FROM TRENDING WHERE HYPE_ID = %s"""
             cursor.execute(query,(hype_id))
             trending_count = cursor.fetchall()
             if rehype_count[0][0] >= 3 :
                 if trending_count[0][0] > 0:
                     return True

    def Decision_Delete(self, hype_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             hype_id = str(hype_id)
             cursor = connection.cursor()
             query = """ SELECT COUNT(*) FROM REHYPES WHERE HYPE_ID = %s"""
             cursor.execute(query,(hype_id))
             rehype_count = cursor.fetchall()
             cursor = connection.cursor()
             query = """ SELECT COUNT(*) FROM TRENDING WHERE HYPE_ID = %s"""
             cursor.execute(query,(hype_id))
             trending_count = cursor.fetchall()
             if rehype_count[0][0] < 3 :
                 if trending_count[0][0] > 0:
                     return True

    def Add_Trending(self, hype_id, rehype_count, word):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                cursor = connection.cursor()
                query =  """INSERT INTO TRENDING(HYPE_ID, TAG, DATE, COUNT) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (hype_id, word, date, rehype_count))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Update_Trending(self, hype_id, incOrDec):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                hype_id = str(hype_id)
                cursor = connection.cursor()
                query = """ SELECT COUNT FROM TRENDING WHERE HYPE_ID = %s"""
                cursor.execute(query,(hype_id))
                count = cursor.fetchall()
                if incOrDec == 1:
                    count = count[0][0] + 1
                elif incOrDec == 2:
                    count = count[0][0] - 1
                hype_id = int(hype_id)
                cursor = connection.cursor()
                query =  """UPDATE TRENDING
                             SET COUNT = %s
                             WHERE (HYPE_ID = %s)"""
                cursor.execute(query, (count, hype_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Delete_Trending(self, hype_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                hype_id = str(hype_id)
                cursor = connection.cursor()
                query =  """DELETE FROM TRENDING WHERE (HYPE_ID = %s)"""
                cursor.execute(query, (hype_id,))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
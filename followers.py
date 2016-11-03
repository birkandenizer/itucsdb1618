import psycopg2 as dbapi2
import datetime

class followers:
    def __init__(self, app):
        self.app = app

    def show_followers(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM FOLLOWER """
             cursor.execute(query)
             sportpage = cursor.fetchall()
             return sportpage


    def select_followers(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM HYPES WHERE TOPIC='Sport' ORDER BY DATE ASC"""
             cursor.execute(query)
             sportpage = cursor.fetchall()
             return sportpage

    def update_group(self, person_id, follower_id, group_name):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """UPDATE FOLLOWER SET GROUP_NAME = %s WHERE PERSON_ID=%s AND FOLLOWER_ID=%s"""
                cursor.execute(query, (group_name, person_id, follower_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()


    def add_follow(self, person_id, follower_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                cursor = connection.cursor()
                group_name= "General"
                query =  """INSERT INTO FOLLOWER(PERSON_ID, FOLLOWER_ID, GROUP_NAME, DATE) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (person_id, follower_id, group_name, date))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()


    def delete_follow(self, follower_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM FOLLOWER WHERE (FOLLOWER_ID = %s)"""
                cursor.execute(query, (follower_id,))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()




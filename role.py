import psycopg2 as dbapi2

class Role:
    def __init__(self, app):
        self.app = app

    def List_Roles(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM ROLES"""
             cursor.execute(query)
             roles = cursor.fetchall()
             return roles

    def Add_Roles(self, user_id, tag, type):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """INSERT INTO ROLES(USER_ID, TAG, TYPE) VALUES (%s, %s, %s)"""
                cursor.execute(query, (user_id, tag, type))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Delete_Roles(self, id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM ROLES WHERE (ID = %s)"""
                cursor.execute(query, (id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Update_Roles(self, id, tag, type):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """UPDATE ROLES SET TAG = %s, TYPE = %s WHERE ID = %s"""
                cursor.execute(query, (tag, type, id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
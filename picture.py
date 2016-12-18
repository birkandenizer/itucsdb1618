import psycopg2 as dbapi2

class Picture:
    def __init__(self, app):
        self.app = app

    def initialize_table(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS PICTURE (
                PICTURE_ID               INT             PRIMARY KEY     NOT NULL,
                USER_ID                  INT                             NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                URL                      VARCHAR(100)                    NOT NULL
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
                query = """DROP TABLE IF EXISTS PICTURE"""
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def list_pictures(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM PICTURE ORDER BY PICTURE_ID"""
             cursor.execute(query)
             picturesspage = cursor.fetchall()
             return picturesspage
            
    def get_url(self, user_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "SELECT URL FROM PICTURE WHERE USER_ID = '" + str(user_id) + "'"
                cursor.execute(query)
                url = cursor.fetchall()
                if  url is None:
                    url = "{{url_for('static', filename='avatar-1577909_1280.png')}}"
                    return url
                else:
                    url=url[0][0]
                    return url
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def add_picture(self, picture_id, user_id, url):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """INSERT INTO PICTURE(PICTURE_ID, USER_ID, URL) VALUES (%s,%s,%s)"""
                cursor.execute(query, (picture_id, user_id, url))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def delete_picture(self, picture_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM PICTURE WHERE (PICTURE_ID = %s)"""
                cursor.execute(query, (picture_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def update_picture(self, picture_id, url):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """UPDATE PICTURE SET URL = %s WHERE PICTURE_ID = %s"""
                cursor.execute(query, (url, picture_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

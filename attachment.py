import psycopg2 as dbapi2

class Attachment:
    def __init__(self, app):
        self.app = app

    def initialize_table(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS ATTACHMENT (
                ATTACHMENT_ID            INT             PRIMARY KEY     NOT NULL,
                HYPE_ID                  INT                             NOT NULL REFERENCES HYPES (HYPE_ID) ON DELETE CASCADE,
                ATTACHMENT_TYPE          VARCHAR(10)                     NOT NULL,
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
                query = """DROP TABLE IF EXISTS ATTACHMENT"""
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def list_attachments(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM ATTACHMENT ORDER BY ATTACHMENT_ID"""
             cursor.execute(query)
             attachmentspage = cursor.fetchall()
             return attachmentspage

    def add_attachment(self, attachment_id, hype_id, attachment_type, url):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """INSERT INTO ATTACHMENT(ATTACHMENT_ID, HYPE_ID, ATTACHMENT_TYPE, URL) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (attachment_id, hype_id, attachment_type, url))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def delete_attachment(self, attachment_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM ATTACHMENT WHERE (ATTACHMENT_ID = %s)"""
                cursor.execute(query, (attachment_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def update_attachment(self, attachment_id, attachment_type, url):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """UPDATE ATTACHMENT SET ATTACHMENT_TYPE = %s, URL = %s WHERE ATTACHMENT_ID = %s"""
                cursor.execute(query, (attachment_type, url, attachment_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

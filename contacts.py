import psycopg2 as dbapi2

class contact:
    def __init__(self, ticket_id, subject, name, surname, email, message):
        self.ticket_id = ticket_id
        self.subject=subject
        self.name = name
        self.surname = surname
        self.email = email
        self.message = message

class Contact:
    def __init__(self, app):
        self.app = app

    def initialize_table(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS CONTACT (
                TICKET_ID    INT PRIMARY KEY NOT NULL,
                SUBJECT     VARCHAR(20) NOT NULL,
                NAME        VARCHAR(20) NOT NULL,
                SURNAME     VARCHAR(20) NOT NULL,
                EMAIL       VARCHAR(30) NOT NULL,
                MESSAGE   VARCHAR(200) NOT NULL
                )""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def list_contacts(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             try:
                 cursor = connection.cursor()
                 query = """ SELECT * FROM CONTACT ORDER BY TICKET_ID"""
                 cursor.execute(query)
                 contacts = cursor.fetchall()
                 return contacts
             except dbapi2.DatabaseError:
                connection.rollback()
             finally:
               connection.commit()

    def add_contact(self, ticket_id, subject, name, surname, email, message):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO CONTACT (TICKET_ID, SUBJECT,NAME,SURNAME,EMAIL,MESSAGE) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (ticket_id, subject, name, surname, email, message))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
    def get_contact(self, ticket_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """ SELECT * FROM CONTACT WHERE TICKET_ID = %s """
                cursor.execute(query, (ticket_id))
                contact = cursor.fetchall()
                return contact
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
    def update_contact(self, subject, name, surname, email, message, ticket_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """ UPDATE CONTACT SET SUBJECT = %s,NAME = %s,SURNAME = %s,EMAIL = %s,MESSAGE = %s WHERE TICKET_ID = %s"""
                cursor.execute(query, (subject, name, surname, email, message, ticket_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
    def delete_contact(self, ticket_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM CONTACT WHERE TICKET_ID = %s"""
                cursor.execute(query, (ticket_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
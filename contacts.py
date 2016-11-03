import psycopg2 as dbapi2

from contact import contact

class store_contact:
    def __init__(self, app):
        self.app = app

    def add_contact(self, subject, name, surname, email, message, ticket_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO CONTACT (SUBJECT,NAME,SURNAME,EMAIL,MESSAGE,TICKET_ID) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (subject, name, surname, email, message, ticket_id))
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
                cursor.execute(query, [ticket_id])
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
                query = """ UPDATE CONTACTS WHERE TICKET_ID = %s
                        SUBJECT = %s,NAME = %s,SURNAME = %s,EMAIL = %s,MESSAGE = %s, TICKET_ID = %s """
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
                query =  """DELETE FROM CONTACT WHERE (TICKET_ID = ?)"""
                cursor.execute(query, (ticket_id,))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
    def select_contact(self):
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
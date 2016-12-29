Parts Implemented by Birkan Denizer
===================================
In this website project, I created picture, attachment and contact entities and their respective operations. All these tables support basic operations such as add, select, update and so on.

* Initialize table
      Creates table
* Drop table
      Deletes table
* Add
      Adds a new entry into table
* Get
      Returns a single entry which conforms to given parameter from table
* List
      Returns all entries which conform to given parameters  from table
* Update
      Updates a single entry which conforms to given parameter from table
* Delete
      Deletes a single entry which conforms to given parameter from table

Attachment table and relevant operations
----------------------------------------
After adding hypes, user is redirected to attachment page. In the attachments page, you can enter attachment_type and url of the attachment and these informations are passed by a form to corresponding app.route in server.py.
ATTACHMENT table has following columns

* *ATTACHMENT_ID* as integer
   This column is our primary key in this table
* *HYPE_ID* as integer
   This column takes HYPE_ID from HYPES table and is a foreign key
* *ATTACHMENT_TYPE* as varchar
   This column is type of added attachment such as PNG,JPEG,PDF etc.
* *URL* as varchar
   This column is our link to specified attachment


*Initialize table*
^^^^^^^^^^^^^^^^^^
This part *CREATE*s necessary ATTACHMENT table for operations

.. code-block:: python

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


*Drop table*
^^^^^^^^^^^^
This part *DELETE*s ATTACHMENT table

.. code-block:: python

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


*Add*
^^^^^
This part *INSERT*s a new entry to ATTACHMENT table

.. code-block:: python

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


*List*
^^^^^^
This part returns all entries in ATTACHMENT table by *SELECT*

.. code-block:: python

   def list_attachments(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM ATTACHMENT ORDER BY ATTACHMENT_ID"""
             cursor.execute(query)
             attachmentspage = cursor.fetchall()
             return attachmentspage


*Update*
^^^^^^^^
This part *UPDATE*s the relevant entry in ATTACHMENT table

.. code-block:: python

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


*Delete*
^^^^^^^^
This part *DELETE*s the relevant entry in ATTACHMENT table

.. code-block:: python

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


Contact table and relevant operations
-------------------------------------
Anyone having problems can contact support. In the contact page, you can enter subject, name, surname, email and message. These informations are passed by a form to corresponding app.route in server.py.
To store this information, a class is implemented. CONTACT table has following columns

* *TICKET_ID* as integer
   This column is our primary key in this table
* *SUBJECT* as varchar
   This column holds subject of message
* *NAME* as varchar
   This column holds name of message's sender
* *SURNAME* as varchar
   This column holds surname of message's sender
* *EMAIL* as varchar
   This column holds email of message's sender
* *MESSAGE* as varchar
   This column holds message

*Initialize table*
^^^^^^^^^^^^^^^^^^
This part *CREATE*s necessary CONTACT table for operations

.. code-block:: python

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


*Drop table*
^^^^^^^^^^^^
This part *DELETE*s CONTACT table

.. code-block:: python

   def drop_table(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """DROP TABLE IF EXISTS CONTACT"""
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()


*Add*
^^^^^
This part *INSERT*s a new entry to CONTACT table

.. code-block:: python

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


*Get*
^^^^^
This part return a single entry in CONTACT table by *SELECT*


.. code-block:: python

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


*List*
^^^^^^
This part returns all entries in CONTACT table by *SELECT*

.. code-block:: python

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


*Update*
^^^^^^^^
This part *UPDATE*s the relevant entry in CONTACT table

.. code-block:: python

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


*Delete*
^^^^^^^^
This part *DELETE*s the relevant entry in CONTACT table

.. code-block:: python

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



Picture table and relevant operations
-------------------------------------
After sign up, user is redirected to picture page. In the pictures page, you can enter url of the picture and this information is passed by a form to corresponding app.route in server.py. These pictures are presented in profile pages and in hypelines.
PICTURE table has following columns

* *PICTURE_ID* as integer
   This column is our primary key in this table
* *USER_ID* as integer
   This column takes USER_ID from USER table and is a foreign key
* *URL* as varchar
   This column is our url for picture


*Initialize table*
^^^^^^^^^^^^^^^^^^
This part *CREATE*s necessary PICTURE table for operations

.. code-block:: python

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


*Drop table*
^^^^^^^^^^^^
This part *DELETE*s PICTURE table

.. code-block:: python

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


*Add*
^^^^^
This part *INSERT*s a new entry to PICTURE table

.. code-block:: python

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


*Get*
^^^^^
This part return URL of a single entry in PICTURE table by *SELECT*


.. code-block:: python

   def get_url(self, user_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "SELECT URL FROM PICTURE WHERE USER_ID = '" + str(user_id) + "'"
                cursor.execute(query)
                url = cursor.fetchall()
                if  url==[]:
                    url = "https://raw.githubusercontent.com/itucsdb1618/itucsdb1618/master/static/avatar-1577909_1280.png"
                    return url
                else:
                    url=url[0][0]
                    return url
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()


*List*
^^^^^^
This part returns all entries in PICTURE table by *SELECT*

.. code-block:: python

   def list_pictures(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = """ SELECT * FROM PICTURE ORDER BY PICTURE_ID"""
             cursor.execute(query)
             picturesspage = cursor.fetchall()
             return picturesspage


*Update*
^^^^^^^^
This part *UPDATE*s the relevant entry in PICTURE table

.. code-block:: python

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


*Delete*
^^^^^^^^
This part *DELETE*s the relevant entry in PICTURE table

.. code-block:: python

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


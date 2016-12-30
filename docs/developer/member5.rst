Parts Implemented by Cumali Abalık
================================

I implemented Follower, Dislike  and Block Hype entities for our project.

Follower Table and Its Implementations
--------------------------------------
This table shows which user follows which users or simply users connections. 

**Note:** For listing user own hypes on hypeline and account page, user follows himself/herself when creating new user. User can see hypes of only users that are follows or himself/herself.

+------------+---------+----------+-------------+-----------+
| Attribute  | Type    | Not Null | Primary key | Reference |
+============+=========+==========+=============+===========+
| PERSON_ID  | INTEGER | 1        | No          | Yes       |
+------------+---------+----------+-------------+-----------+
| FOLLOWER_ID| INTEGER | 1        | No          | Yes       |
+------------+---------+----------+-------------+-----------+
| GROUP_NAME | VARCHAR | 0        | No          | No        |
+------------+---------+----------+-------------+-----------+
| DATE       | DATE    | 1        | No          | No        |
+------------+---------+----------+-------------+-----------+

   - *PERSON_ID* is user who follows another user
   - *FOLLOWER_ID* user who followed by another one
   - *GROUP_NAME* Group of following. User can divide followings by group name
   - *DATE* date of following time
   
**SQL statement for followers class :**

.. code-block:: python

              class followers:
                def __init__(self, app):
                  self.app = app
   
**SQL statement for creating the follower  table :**

.. code-block:: python

            def initialize_table(self):
               with dbapi2.connect(self.app.config['dsn']) as connection:
                  try:
                      cursor = connection.cursor()
                      cursor.execute(""" CREATE TABLE IF NOT EXISTS FOLLOWER(
                      PERSON_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                      FOLLOWER_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                      GROUP_NAME VARCHAR(50),
                      DATE DATE NOT NULL,
                      PRIMARY KEY(PERSON_ID,FOLLOWER_ID)
                      )""")
                      connection.commit()
                  except dbapi2.DatabaseError:
                      connection.rollback()
                  finally:
                     connection.commit()

**SQL statement for dropping the follower  table :**

.. code-block:: python

              def drop_table(self):
                with dbapi2.connect(self.app.config['dsn']) as connection:
                    try:
                        cursor = connection.cursor()
                        query = """DROP TABLE IF EXISTS FOLLOWER"""
                        cursor.execute(query)
                    except dbapi2.DatabaseError:
                        connection.rollback()
                    finally:
                       connection.commit()

**SQL statement for Adding the follower  table :**

.. code-block:: python

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
      
**SQL statement for delete the follower  table :**

.. code-block:: python  

              def delete_follow(self, person_id, follower_id):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          cursor = connection.cursor()
                          query =  """DELETE FROM FOLLOWER WHERE PERSON_ID = %s AND FOLLOWER_ID = %s"""
                          cursor.execute(query, (person_id, follower_id,))
                          connection.commit()
                          cursor.close()
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()
      
**SQL statement for update the follower  table :**

User can update the group name of following connection. User can divide groups such as friend, family following connection.

.. code-block:: python          

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
      
**SQL statement for Listing Hypes for follower  table :**

This python code is listing hypes that topic is Sport.

.. code-block:: python        

              def select_followers(self):
                with dbapi2.connect(self.app.config['dsn']) as connection:
                     cursor = connection.cursor()
                     query = """ SELECT * FROM HYPES WHERE TOPIC='Sport' ORDER BY DATE ASC"""
                     cursor.execute(query)
                     sportpage = cursor.fetchall()
                     return sportpage
      
**SQL statement for Listing follower  table :**

.. code-block:: python 

              def show_followers(self):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                       cursor = connection.cursor()
                       query = """ SELECT * FROM FOLLOWER """
                       cursor.execute(query)
                       sportpage = cursor.fetchall()
                       return sportpage


Blocked Table and Its Implementations
--------------------------------------
This table implements blocking users by user.

+------------+---------+----------+-------------+-----------+
| Attribute  | Type    | Not Null | Primary key | Reference |
+============+=========+==========+=============+===========+
| PERSON_ID  | INTEGER | 1        | No          | Yes       |
+------------+---------+----------+-------------+-----------+
| BLOCK_ID   | INTEGER | 1        | No          | Yes       |
+------------+---------+----------+-------------+-----------+
| REASON     | VARCHAR | 0        | No          | No        |
+------------+---------+----------+-------------+-----------+
| DATE       | DATE    | 1        | No          | No        |
+------------+---------+----------+-------------+-----------+

   - *PERSON_ID* is user who makes the block
   - *BLOCK_ID* user who blocked
   - *REASON* Reason of blocking.
   - *DATE* date of blocking time
   
**SQL statement for block class :**

.. code-block:: python

              class block:
                  def __init__(self, app):
                      self.app = app

**SQL statement for initialize table of blocked table :**

.. code-block:: python

              def initialize_table(self):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          cursor = connection.cursor()
                          cursor.execute(""" CREATE TABLE IF NOT EXISTS BLOCKED(
                          PERSON_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                          BLOCK_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                          REASON VARCHAR(50),
                          DATE DATE NOT NULL,
                          PRIMARY KEY(PERSON_ID,BLOCK_ID)
                          )""")
                          connection.commit()
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()
                         
**SQL statement for drop table of blocked table :**

.. code-block:: python

              def drop_table(self):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          cursor = connection.cursor()
                          query = """DROP TABLE IF EXISTS BLOCKED"""
                          cursor.execute(query)
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()
                         
**SQL statement for add function for blocked table :**

.. code-block:: python

              def add_block(self, person_id, block_id, reason):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          date = datetime.date.today()
                          cursor = connection.cursor()
                          query =  """INSERT INTO BLOCKED(PERSON_ID, BLOCK_ID, REASON, DATE) VALUES (%s, %s, %s, %s)"""
                          cursor.execute(query, (person_id, block_id, reason, date))
                          connection.commit()
                          cursor.close()
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()
                         
**SQL statement for delete function for blocked table :**

.. code-block:: python

              def delete_block(self, person_id, block_id):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          cursor = connection.cursor()
                          query =  """DELETE FROM BLOCKED WHERE PERSON_ID = %s AND BLOCK_ID = %s"""
                          cursor.execute(query, (person_id, block_id))
                          connection.commit()
                          cursor.close()
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()
                         
**SQL statement for listing blocked tables :**

.. code-block:: python                               

              def show_blocked(self):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                       cursor = connection.cursor()
                       query = """ SELECT * FROM BLOCKED """
                       cursor.execute(query)
                       sportpage = cursor.fetchall()
                       return sportpage     
                       
**SQL statement for update block reason for blocked tables :**

.. code-block:: python 

              def update_reason(self, person_id, block_id, reason):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          cursor = connection.cursor()
                          query =  """UPDATE BLOCKED SET REASON = %s WHERE PERSON_ID=%s AND BLOCK_ID=%s"""
                          cursor.execute(query, (reason, person_id, block_id))
                          connection.commit()
                          cursor.close()
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()
                    
                    
Dislikes Table and Its Implementations
--------------------------------------
This table implements blocking users by user.

+------------+---------+----------+-------------+-----------+
| Attribute  | Type    | Not Null | Primary key | Reference |
+============+=========+==========+=============+===========+
| ID         | SERIAL  | 1        | Yes         | No        |
+------------+---------+----------+-------------+-----------+
| HYPE_ID    | INTEGER | 1        | No          | Yes       |
+------------+---------+----------+-------------+-----------+
| USER_ID    | INTEGER | 1        | No          | Yes       |
+------------+---------+----------+-------------+-----------+
| REASON     | VARCHAR | 0        | No          | No        |
+------------+---------+----------+-------------+-----------+
| DATE       | DATE    | 1        | No          | No        |
+------------+---------+----------+-------------+-----------+
   
   - *id* is the primary key
   - *HYPE_ID* hype which one will be dislike
   - *USER_ID* is user who makes the dislike
   - *REASON* Reason of dislike.
   - *DATE* date of blocking time
   
**SQL statement for dislike class :**

.. code-block:: python  

              class dislike:
                  def __init__(self, app):
                      self.app = app
                      
**SQL statement for initialize table of dislikes table :**

.. code-block:: python   

              def initialize_table(self):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          cursor = connection.cursor()
                          cursor.execute(""" CREATE TABLE IF NOT EXISTS DISLIKES(
                          ID SERIAL PRIMARY KEY,
                          HYPE_ID INTEGER NOT NULL REFERENCES HYPES (HYPE_ID) ON DELETE CASCADE,
                          USER_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                          DATE DATE NOT NULL,
                          REASON VARCHAR(50),
                          UNIQUE(HYPE_ID,USER_ID)
                          )""")
                          connection.commit()
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()

**SQL statement for drop table of dislikes table :**

.. code-block:: python   

              def drop_table(self):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          cursor = connection.cursor()
                          query = """DROP TABLE IF EXISTS DISLIKES"""
                          cursor.execute(query)
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()
                         
**SQL statement for listing hypes  :**

.. code-block:: python

              def List_Hypes(self):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                       cursor = connection.cursor()
                       query = """ SELECT * FROM HYPES ORDER BY HYPES"""
                       cursor.execute(query)
                       dislike_hypes = cursor.fetchall()
                       return dislike_hypes
                       
**SQL statement for listing dislikes table  :**

.. code-block:: python

              def select_dislikes(self):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                       cursor = connection.cursor()
                       query = """ SELECT * FROM DISLIKES """
                       cursor.execute(query)
                       users_dislike = cursor.fetchall()
                       return users_dislike
                       
**SQL statement for adding dislikes for dislikes table  :**

.. code-block:: python

              def add_dislike(self, user_id, hype_id, reason):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          date = datetime.date.today()
                          cursor = connection.cursor()
                          query =  """INSERT INTO DISLIKES(HYPE_ID, USER_ID, DATE, REASON) VALUES (%s, %s, %s, %s)"""
                          cursor.execute(query, (hype_id, user_id, date, reason))
                          connection.commit()
                          cursor.close()
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()
                       
**SQL statement for deleting dislikes from dislikes table  :**

.. code-block:: python

              def delete_dislike(self, hype_id, user_id):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          cursor = connection.cursor()
                          query =  """DELETE FROM DISLIKES WHERE HYPE_ID = %s AND USER_ID = %s"""
                          cursor.execute(query, (hype_id, user_id))
                          connection.commit()
                          cursor.close()
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()

**SQL statement for update dislikes reason from dislikes table  :**

.. code-block:: python

              def update_reason(self, hype_id, user_id, reason):
                  with dbapi2.connect(self.app.config['dsn']) as connection:
                      try:
                          cursor = connection.cursor()
                          query =  """UPDATE DISLIKES SET REASON = %s WHERE HYPE_ID=%s AND USER_ID=%s"""
                          cursor.execute(query, (reason, hype_id, user_id))
                          connection.commit()
                          cursor.close()
                      except dbapi2.DatabaseError:
                          connection.rollback()
                      finally:
                         connection.commit()
                         
                       

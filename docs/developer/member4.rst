Parts Implemented by Bora Ünal
================================

REHYPE PART / TRENDING PART
~~~~~~~~~~~~~~~~~~
All hypes areas have rehype button to add them rehype table. Rhypes table is used to share the entered hype with others. Adding, deleting, updating and listing operation is made for rehype tables.

Trending table is used to keep hypes which is rehyped many times. Also the user who want to see only tag inside hype text, can do it tag links.

* Create Rehype

.. code-block:: python

   def initialize_Rehype(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(""" CREATE TABLE IF NOT EXISTS REHYPES(
                HYPE_ID INTEGER NOT NULL REFERENCES HYPES (HYPE_ID) ON DELETE CASCADE,
                USER_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                COMMENT VARCHAR(200),
                DATE DATE NOT NULL,
                PRIMARY KEY (HYPE_ID, USER_ID)
                )""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
               
Rehype table has two foreign keys, these keys are also primary key. 

* Create Trending

.. code-block:: python

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
               
Trending table has id primary key, one foreign key and one unique. Hype_id also unique to see the same hype only once.

* Add Rehype

.. code-block:: python

   def music_page_add(hype_id):
       app.rehype.Add_Rehype(session['userid'], hype_id)
       return render_template('rehypes.html', rehypespage = app.rehype.List_RehypesUser(session['userid']))
      
Music page add function takes hype_id as a parameter, then it sent user_id, hype_id to Add_Rehype function in rehype.py. Add_Rehype fuction added new record to database. Lastl, music_page_add function lists all hypes in music page.

.. code-block:: python

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
               
Comment is initially taken as a constant, then updated.

* Add Trending

.. code-block:: python

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

* Delete Rehype / Delete Trending / Update Trending

.. code-block:: python

   def music_page_delete(hype_id):
      hype_ids = app.rehype.Delete_Rehype(session['userid'], hype_id)
      element = False
      element = app.trending.Decision_Delete(hype_ids)
      if element == True:
          app.trending.Delete_Trending(hype_ids)
      element = False
      element = app.trending.Decision_Update_Del(hype_ids)
      if element == True:
          app.trending.Update_Trending(hype_ids, 2)
      rehypesUser = app.rehype.List_Users()
      return render_template('rehypes_list.html', rehypespage = app.rehype.List_RehypesUser(session['userid']), rehypesUser = rehypesUser)

Music page delete function takes hype_id as a parameter, then it sends user_id, hype_id variable to Delete rehype function in rehype.py. After delete operation, function check rehype's count in the trending table. If reype's count is less than 3 then hype's tag is removed from trending table with Delete Trending function, otherwise only count is updated in trending.py

.. code-block:: python

   def Delete_Rehype(self, user_id, hype_ids):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """ SELECT HYPE_ID FROM REHYPES WHERE USER_ID = %s"""
                cursor.execute(query,(user_id))
                hype_id = cursor.fetchall()
                cursor = connection.cursor()
                query =  """DELETE FROM REHYPES WHERE (USER_ID = %s) AND (HYPE_ID = %s)"""
                cursor.execute(query, (user_id, hype_ids,))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
                return hype_ids
            finally:
               connection.commit()
               return hype_ids
               
.. code-block:: python

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
               
.. code-block:: python

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
               
IncorDec variable is used to decide whether Update Trending funnction is called from delete rhype or update rehype. If it called from delete rehype then incorDec is equal to 2. Therefore trending table's count is decremented. If it called from update rehype then incorDec is equal to 1. Therefore trending table's count is incremented.

* List Rehype

.. code-block:: python 

   def rehypes_list():
      user_ids = session['userid']
      rehypespage = app.rehype.List_RehypesUser(user_ids)
      rehypesUser = app.rehype.List_Users()
      return render_template('rehypes_list.html', rehypespage = rehypespage, rehypesUser = rehypesUser)
        
Rehype list function takes user_id in session to show only logined user's rehype list. Then the list which be returned from RehypesUser is sent to rehypes html.

.. code-block:: python

   def List_RehypesUser(self, user_ids):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             user_ids = str(user_ids)
             cursor = connection.cursor()
             query = """ SELECT * FROM REHYPES WHERE USER_ID = %s ORDER BY DATE ASC"""
             cursor.execute(query,(user_ids))
             rehypespage = cursor.fetchall()
             return rehypespage
             
             
FAVORITE PART
~~~~~~~~~~~~~~~~~~
All hypes areas have rehype button to add them rehype table. Favorites table keep popular hypes for users. Also user can give vote them to list them on top rated. Adding, deleting, updating and listing operation is made for favorites tables.

* Create Favorite

.. code-block:: python

   def initialize_Favorite(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(""" CREATE TABLE IF NOT EXISTS FAVORITES(
                ID SERIAL PRIMARY KEY,
                HYPE_ID INTEGER NOT NULL REFERENCES HYPES (HYPE_ID) ON DELETE CASCADE,
                USER_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                DATE DATE NOT NULL,
                RATE INTEGER NOT NULL,
                UNIQUE(HYPE_ID,USER_ID)
                )""")
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
Favorite table has primary key, two foreign key and unique. Hype_id and user_id are unique therefore same user does not add same hype twice.

* Add Favorite

.. code-block:: python

   def favorite_add():
    if request.method == 'GET':
        hypespageUsername = app.rehype.List_Users()
        return render_template('music.html', hypespage = app.rehype.List_Hypes(), hypespageUsername = hypespageUsername)
    else:
        hype_id = request.form['hype_id']
        user_ids = session['userid']
        app.favorite.Add_Favorite(user_ids, hype_id)
        hypespageUsername = app.rehype.List_Users()
        return render_template('music.html', hypespage = app.rehype.List_Hypes(), hypespageUsername = hypespageUsername)
        
Favorite add function gets hype_id from form and user.id from session. Then this variable is sent to Add Favorite function in favorites.py. After new record is added, function redirects users to music page.

.. code-block:: python

   def Add_Favorite(self, user_ids, hype_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                date = datetime.date.today()
                rate = 1
                cursor = connection.cursor()
                query =  """INSERT INTO FAVORITES(HYPE_ID, USER_ID, DATE, RATE) VALUES (%s, %s, %s, %s)"""
                cursor.execute(query, (hype_id, user_ids, date, rate))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
               
* Delete Favorites

.. code-block:: python

   def favorite_delete(favorite_id):
      app.favorite.Delete_Favorite(favorite_id)
      user_ids = session['userid']
      favorites = app.favorite.List_Favorites(user_ids)
      rehypesUser = app.rehype.List_Users()
      return render_template('selectedfavorites.html', favorites=favorites, rehypesUser=rehypesUser)
      
Favorite delete function takes favorite_id which user want to delete, as a parameter. Then favorite_id is sent to Delete favorite function in favorites.py. After record is deleted, list of favorites table is kept favorites variable. Lastly, function redirects user to favorite list page.

.. code-block:: python

   def Delete_Favorite(self, favorite_id):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """DELETE FROM FAVORITES WHERE (ID = %s)"""
                cursor.execute(query, (favorite_id,))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
               
* Update Favorites

.. code-block:: python

   def favorite_update(favorite_id):
    if request.method == 'GET':
        favorites=app.favorite.List_FavoritesID(favorite_id)
        return render_template('favorite_update.html', favorites=favorites)
    else:
        favorite_id = request.form['favorite_id']
        rate = request.form['rate']
        app.favorite.Update_Favorite(favorite_id, rate)
        user_ids = session['userid']
        favorites = app.favorite.List_Favorites(user_ids)
        rehypesUser = app.rehype.List_Users()
        return render_template('selectedfavorites.html', favorites=favorites, rehypesUser=rehypesUser)
        
Favorite update function takes favorite_id as a parameter for listing. When it updating table, it take favorite_id and rate from form. Then it redirect user to favorite list page.

.. code-block:: python

   def Update_Favorite(self, favorite_id, rate):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query =  """UPDATE FAVORITES
                             SET RATE = %s
                             WHERE (ID = %s)"""
                cursor.execute(query, (rate, favorite_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

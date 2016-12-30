Parts Implemented by Onat Uner
================================

 .. code-block:: python
 
        @app.route('/hypeline')
        def hypeline_page():
            return render_template('hypeline.html', hypes = app.hypeline.List_Hypes_Hypeline(session['userid']), url = app.picture.get_url(session['userid']))

        @app.route('/hypeline/hype', methods=['POST'])
        def hypeline_hype():
            t = datetime.date.today()
            text = request.form['hype_text']
            topic = request.form['topic']
            tags = request.form['hype_tag']

        app.hype.Add_Hype(session['userid'], t, text, topic)
        hype_id=app.hype.Get_Hype_ID(session['userid'], t, text, topic)
        app.hype.Add_Tags(hype_id, t, tags)

        return redirect(url_for('hypeline_page'))
    
hypeline_hype() function gets the required information from the hypeline.html and calls the Add_Hype() function to create a new entry in the HYPES table. Then the HYPE_ID of the inserted entry is taken with the Get_Hype_ID() function.
This HYPE_ID is used for adding the tags to that hype with the Add_Tags() funtion.

 .. code-block:: python
 
        @app.route('/hype')
        def hype_page():
            hypes=app.hype.Select_All_Hypes()
            return render_template('hype.html', hypes = hypes)
/hype:
Here the operations on HYPES table is implemented. Input from the user is gathered and sent to the relevant function to carry out the operation. The main html used here is the hype.html. This page's outlook can be seen in the user manual.
hype_page() is the main template that functions return after their operation. Here all the entries in the table are shown for default.

 .. code-block:: python
 
        @app.route('/addHype', methods=['POST'])
        def hype():
            user_id = request.form['user_id']
            t = datetime.date.today()
            text = request.form['hype_text']
            topic = request.form['topic']
            tags = request.form['hype_tag']

            app.hype.Add_Hype(user_id, t, text, topic)
            hype_id=app.hype.Get_Hype_ID(user_id, t, text, topic)
            app.hype.Add_Tags(hype_id, t, tags)

            return render_template("attachment.html", hype_id=hype_id)

hype() is the operation that adds a new entry for the HYPES table. The required information is taken from the html using forms and then used for creating a new entry through different functions. USER_ID is taken from the session, the user has to log in before submitting a hype and date information is taken from the server using the datetime library. After that attachment.html is rendered.


 .. code-block:: python
 
        @app.route('/commentHype', methods=['POST'])
        def comment_hype():
            hype_id = request.form['comment_hype_id']
            user_id = request.form['comment_user_id']
            t = datetime.date.today()
            text = request.form['comment_text']
            app.hype.Comment_Hype(hype_id, user_id, t, text)

            return redirect(url_for('hype_page'))

comment_hype() is the operation that adds a new entry for the COMMENTS table. The required information is processed using the same way with hype().


 .. code-block:: python
 
        @app.route('/editHype', methods=['POST'])
        def edit_hype():
            with dbapi2.connect(app.config['dsn']) as connection:
                hype_id = request.form['update_hype_id']
                text = request.form['update_hype_text']
                cursor = connection.cursor()
                query = "UPDATE HYPES SET TEXT = '"+ text +"' WHERE HYPE_ID =" + str(hype_id)
                cursor.execute(query)

            return redirect(url_for('hype_page'))

edit_hype() operation allows user to edit a hype of their choosing. The HYPE_ID's are shown in a drop down menu by the html. The required information is processed using the same way with hype().

 .. code-block:: python
 
        @app.route('/deleteHype', methods=['POST'])
        def delete_hype():
            with dbapi2.connect(app.config['dsn']) as connection:
                hype_id = request.form['delete_hype_id']
                cursor = connection.cursor()
                query = "DELETE FROM HYPES WHERE HYPE_ID =" + str(hype_id)
                cursor.execute(query)
            return redirect(url_for('hype_page'))

delete_hype() operation allows user to delete a hype of their choosing. The HYPE_ID's are shown in a drop down menu by the html. After the HYPE_ID is selected this operation removes the entry with that ID from the table.


 .. code-block:: python
    
        @app.route('/selectHype', methods=['POST'])
        def select_hype():
            with dbapi2.connect(app.config['dsn']) as connection:
                hype_id = request.form['select_hype_id']
                cursor = connection.cursor()
                query = "SELECT * FROM HYPES WHERE HYPE_ID =" + str(hype_id)
                cursor.execute(query)
                selectedHype = cursor.fetchall()
            return redirect(url_for('hype_page'))

select_hype() operation allows user to select one hype and display it. The HYPE_ID's are shown in a drop down menu by the html. After the HYPE_ID is selected this operation that hype is shown.


hypes.py keeps all the functions for the HYPES, COMMENTS and TAGS tables:

.. code-block:: python

    def Initialize_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """CREATE TABLE IF NOT EXISTS HYPES (
                           HYPE_ID         SERIAL        PRIMARY KEY    NOT NULL,
                           USER_ID         INT                          REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                           DATE            DATE                         NOT NULL,
                           TEXT            VARCHAR(150)                 NOT NULL,
                           TOPIC           VARCHAR(20)                  NOT NULL
                           )"""
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Drop_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "DROP TABLE IF EXISTS HYPES"
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

Initialize_Hypes() function creates the HYPES table if it is not initialized. In this table HYPE_ID is the primary key and is generated automatically with the SERIAL keyword. USER_ID refers to the USERS table and stores which user has submitted the hype.
Drop_Hypes() function drops the table HYPES.

.. code-block:: python

    def Initialize_Comments(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """CREATE TABLE IF NOT EXISTS COMMENTS (
                           COMMENT_ID      SERIAL    PRIMARY KEY   NOT NULL,
                           HYPE_ID         INT       REFERENCES    HYPES(HYPE_ID)    ON DELETE CASCADE,
                           USER_ID         INT                     NOT NULL,
                           DATE            DATE                    NOT NULL,
                           TEXT            VARCHAR(150)            NOT NULL
                           )"""
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Drop_Comments(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "DROP TABLE IF EXISTS COMMENTS"
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

Initialize_Comments() function creates the COMMENTS table if it is not initialized. In this table COMMENT_ID is the primary key and is generated automatically with the SERIAL keyword. HYPE_ID refers to the HYPES table and stores which hype was commented.
Drop_Comments() function drops the table COMMENTS.

.. code-block:: python

    def Initialize_Tags(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """CREATE TABLE IF NOT EXISTS TAGS (
                           TAG_ID          SERIAL        PRIMARY KEY    NOT NULL,
                           HYPE_ID         INT           REFERENCES     HYPES(HYPE_ID)    ON DELETE CASCADE,
                           DATE            DATE                         NOT NULL,
                           TAGS            VARCHAR(50)                  NOT NULL
                           )"""
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

    def Drop_Tags(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "DROP TABLE IF EXISTS TAGS"
                cursor.execute(query)
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()

Initialize_Tags() function creates the TAGS table if it is not initialized. In this table TAG_ID is the primary key and is generated automatically with the SERIAL keyword. HYPE_ID refers to the HYPES table and stores which hype this tag was added.
Drop_Tags() function drops the table TAGS.

.. code-block:: python

    def Add_Hype(self, userID, t, text, topic):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """INSERT INTO HYPES(
                           USER_ID,
                           DATE,
                           TEXT,
                           TOPIC)
                           VALUES("""+ str(userID) +",'" + str(t) +"','"+ text +"','"+ topic +"' )"
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

Add_Hype() takes the required information as variables then adds a new entry to the HYPES table using these variables.


.. code-block:: python

    def Get_Hype_ID(self, userID, t, text, topic):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "SELECT HYPE_ID FROM HYPES WHERE USER_ID = '"+ str(userID) +"' AND DATE='" + str(t) +"' AND TEXT='"+ text +"' AND TOPIC='"+ topic +"'"
                cursor.execute(query)
                hype_ID = cursor.fetchone()
                return hype_ID[0]
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

Get_Hype_ID() selects the hype with the given HYPE_ID and returns it.

.. code-block:: python

    def Select_All_Hypes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = "SELECT * FROM HYPES ORDER BY HYPE_ID"
                cursor.execute(query)
                hypes = cursor.fetchall()
                return hypes
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

Select_All_Hypes() selects all the hypes in the HYPES table and returns it.


.. code-block:: python

    def Comment_Hype(self, hypeID, userID, t, text):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """INSERT INTO COMMENTS(
                HYPE_ID,
                USER_ID,
                DATE,
                TEXT)
                VALUES("""+ str(hypeID) +", "+ str(userID) +",'" + str(t) +"','"+ text + "' )"
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

Comment_Hype() takes the required information as variables then adds a new entry to the COMMENTS table using these variables.

.. code-block:: python

    def Add_Tags(self, hypeID, t, tags):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """INSERT INTO TAGS(
                           HYPE_ID,
                           DATE,
                           TAGS)
                           VALUES("""+ str(hypeID) +",'" + str(t) +"','"+ tags +"' )"
                cursor.execute(query)
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
                connection.commit()

Add_Tags() takes the required information as variables then adds a new entry to the TAGS table using these variables.

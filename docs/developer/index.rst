Developer Guide
===============
Installation
____________
**Requirements**
~~~~~~~~~~~~
* Postgresql
* python3.4>
* psycopg2
* flask

**Setting the running environment**
-------------------------------
1. Set running port for postgresql to 5432

2. Create user in postgresql with name='vagrant' and  password='vagrant'

3. Create database for user vagrant with name 'itucsdb1618'


**Run application**
~~~~~~~~~~~~~~~
1. Get our code from github . You can see our git clone address below:

   https://github.com/itucsdb1618/itucsdb1618.git

2. Go to the 'itucsdb1618' folder then execute command below respectively:

   *cd itucsdb1618*

   *python3 server.py*

3. Open a web browser and type this address on address bar:

   *localhost:5000*

4. After open the website, firstly create table with following address:

   *localhost:5000/initdb*

5. Now, you can browse the website.

6. Also, this project is built and run in bluemix,You can browse the website from http://itucsdb1618.mybluemix.net.

Database Design
---------------
   Database design of our projects is implemented separately by each member. 
   
   There are major tables which are Hypes and Users. Also, there are minor tables which use the information provided by these major tables which are Favorites, Dislikes, Rehypes, Hypeblocks, Tags, Trending, Comments, Attachment, Roles, Picture, Blocked User and Follower. Minor tables are referenced as foreign keys to necessary corresponding columns of major tables. Also, there is an independent table which is Contact table. It is getting message from guests on contact page.

Detailed database relations can be seen below:

.. figure:: /static/Entity Relationship Diagram.jpg
   :scale: 50 %
   :alt: ER

   The ER Diagram of our database.

Code
----
This project is implemented by using the combination of PostgreSQL, Python and HTML. The website is run by Flask, the database connection is handled by Psycopg2 and Bootstrap is used for the graphic design of the HTML pages. The maint part of the code is located in "server.py" which contains the routes for Flask which trigger functions for the specified part of the website. The acquisition of input is also handled in "server.py", however the processing of the input and the application of changes to the database is made in seperate Python modules which are located in the main directory alongside "server.py". The Html files which are used in the project to create dynamic web pages are located in the "templates" folder, while the static files such as css files or images are located in the "static" folder.

**Flask Function Triggers**

Flask provides the use of app routes, which can be specified as a certain url, when that url is visited the function listed below that route will be triggered. This project utilizes this feature in order to get input and handle logins and any other kind of activity. For example this is the code for the home page which is triggered when the user visits "/" or basically the website's main directory::

   .. code-block:: python

	@app.route('/')
	def home_page():
	if 'userid' in session:
		if session['userid'] == 0:
			return render_template('home.html')
		return redirect(url_for('hypeline_page'))
	session['userid'] = 0
	return render_template('home.html')




**Create and Drop Functions of the Database**

The database can be initiliazed with visiting the link "/initdb". This triggers the function which sends create table commands through Psycopg2, creating any missing table. This function also adds and admin user with the username "admin" and password "admin".

All tables in the database can be dropped via visiting the link "/dropitucsdb1618". This is implemented as a fast way to dump all data while testing, if anything goes wrong with the database.


**Input Handling**

Input is acquired through forms and buttons, the information is passed onto Python with the help of the Flask code "request.form" for the forms and by redirection to a certain url for the buttons. The forms redirect the user to a certain url such as "/addUser" with the information sent through the POST method, which is then acquired and put into variables in Python as such::

   .. code-block:: python

	@app.route('/addUser', methods=['POST'])
	def add_user():
		username = request.form['username']
		name = request.form['name']
		surname = request.form['surname']
		email = request.form['email']
		password = request.form['password']
		#retype = request.form('retype')
		app.user.Add_Users(username, name, surname, email, password)


The buttons redirect the user to a url which is constructed according to the information given such as "/sport/add/5". The number 5 is representative of the id of the user that the user wants to follow. Then operations are made to add an entry to the followers table. This is done by the help of Flask which allows the passage of variables through the url. This is implemented with the following code::

   .. code-block:: python

	@app.route('/sport/add/<follower_id>')
	def sport_page_add(follower_id):
		app.followers.add_follow(session['userid'], follower_id)


**Entity Modules**

Every entity in the project is handled with its own module. For example "user.py" is used to make changes in the USERS table in the database or the main feature of the project, the hypeline, is handled by using functions in the module "hypeline.py". These modules contain code regarding the processing of the input and the modification of the information in the database. This provides compartmentalization and better organization for the project.

**User Login**

User login is handled with the session module of Flask. A secret key is provided to encrypt the information in the cookies. Whenever a person logs in, the variable "session['userid']" variable is set to the userid of the logged in account, after the password check. Any operation concerning the integrşty of the login credentials is found in "login.py". The function "Get_UserID" checks whether the username exists in the database and whether the password matches the username or not. If the login is unsucessful the function returns -1. Anything related to userid is checked afterwards and operations are not done if it is equal to -1.

**Other parts of the code is explained further in the invidiual sections of the group members.**

.. toctree::

   member1
   member2
   member3
   member4
   member5

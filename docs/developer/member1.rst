Parts Implemented by Utku Öner
================================
TABLES
__________________

USERS
~~~~~~~~~~~~~~~~~~
The USERS table is one of the main tables in the project. It serves many purposes since the project is based on the interaction of one user and another. The USERS table holds information about a user's account such as, username, name, surname, email and password information. These are used at every corner of the project and are referenced by a number of tables. Its primary key is User_Id which is a serial value that is automatically assigned by the database. The username column must also be unique however since every user need its own identity. This eliminates the need for User_Id but it is still implemented because of username changes. If a certain user wants to change their username with ease.

ROLES
~~~~~~~~~~~~~~~~~~
The ROLES table is implemented in order to provide users with roles such as Moderator or Administrator. Roles topic specific, which means a user can be a Moderator in Music and News but not in Technology. There is a topic named Generic which allows global access. So far only the roles in the Generic tag are used in the project. If a certain user tries to access management pages, it is checked whether or not they are listed as "Admin" in the topic "Generic". Its primary key is role_ID which is basically a surrogate key. It is connected to the USERS table and uses the User_Id column.

HYPEBLOCKS
~~~~~~~~~~~~~~~~~~
The HYPEBLOCKS table is implemented in order to specifically block certain hypes that a person does not want to see. The table is connected to USERS and HYPES via their Id columns. Its primary key is a surrogate key named Hypeblock_ID. This table includes a boolean column named Personal which indicates whether the user wants to block this hype for every user or only for themselves. Only administrators and moderators are able to block hypes for other people. 

MODULES
__________________

hypeline.py
~~~~~~~~~~~~~~~~~~
This module handles the listing of hypes. It has 4 main functions which are list_hypes, list_hypes_user, list_hypes_topic, list_hypes_hypeline. List_hypes lists every hype in the database along with the username information of that hype. This is accomplished by joining the HYPES table with the USERS table. The other three functions also list hypes, only difference being added filters. User list function lists hypes sent by a certain user, topic list function lists hypes sent in one topic and finally, the hypeline list function list every hype that is sent by one user and the users that user follows. The hypeline function is accomplishe by using a SQL query with multiple joins which is shown below::

   .. code-block:: python

	query = """SELECT USERNAME, TEXT, TOPIC, HYPES.DATE FROM USERS INNER JOIN 
			FOLLOWER
            ON USERS.USER_ID = FOLLOWER.FOLLOWER_ID INNER JOIN
            HYPES ON HYPES.USER_ID = FOLLOWER.FOLLOWER_ID
            WHERE FOLLOWER.PERSON_ID = %s ORDER BY DATE DESC"""

user.py
~~~~~~~~~~~~~~~~~~
This module handles every operation about the USERS table. Delete, update and insert operations are handled here with 3 different functions. There are 2 functions present for the select operation. The Get_User function retrieves the information about one user while the List_Users function retrieves the information about every user in the database.

role.py
~~~~~~~~~~~~~~~~~~
This module handles every operation about the ROLES table. Delete, update and insert operations are handled here with 3 different functions. There is a function to select all entries as well. One other important function is the Check_Role function. This function check for the role of a certain user in a certain topic. This function is utilized in handling access to the management pages, which are only accessible by certain users with the privilege.

hypeblock.py
~~~~~~~~~~~~~~~~~~
This module handles every operation about the HYPEBLOCKS table. Delete, update and insert operations are handled here with 3 different functions. Another function list all hypeblock entries in the database.

login.py
~~~~~~~~~~~~~~~~~~
This module is implemented in order to handle login requests. It only has one function which checks whether the username is valid and whether the password is a match or not. The function returns -1 if it fails.

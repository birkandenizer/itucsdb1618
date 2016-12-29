Parts Implemented by Member Name
================================

Parts Implemented by Onat Uner

.. figure:: /static/33_hypeline.png
hypeline_hype() function gets the required information from the hypeline.html and calls the Add_Hype() function to create a new entry in the HYPES table. Then the HYPE_ID of the inserted entry is taken with the Get_Hype_ID() function.
This HYPE_ID is used for adding the tags to that hype with the Add_Tags() funtion.

/hype:
Here the operations on HYPES table is implemented. Input from the user is gathered and sent to the relevant function to carry out the operation. The main html used here is the hype.html. This page's outlook can be seen in the user manual.
.. figure:: /static/27_hype_page.png
hype_page() is the main template that functions return after their operation. Here all the entries in the table are shown for default.
.. figure:: /static/26_hype.png
hype() is the operation that adds a new entry for the HYPES table. The required information is taken from the html using forms and then used for creating a new entry through different functions. USER_ID is taken from the session, the user has to log in before submitting a hype and date information is taken from the server using the datetime library. After that attachment.html is rendered.
.. figure:: /static/22_comment_hype.png
comment_hype() is the operation that adds a new entry for the COMMENTS table. The required information is processed using the same way with hype().
.. figure:: /static/24_edit_hype.png
edit_hype() operation allows user to edit a hype of their choosing. The HYPE_ID's are shown in a drop down menu by the html. The required information is processed using the same way with hype().
.. figure:: /static/23_delete_hype.png
delete_hype() operation allows user to delete a hype of their choosing. The HYPE_ID's are shown in a drop down menu by the html. After the HYPE_ID is selected this operation removes the entry with that ID from the table.
.. figure:: /static/32_select_hype.png
select_hype() operation allows user to select one hype and display it. The HYPE_ID's are shown in a drop down menu by the html. After the HYPE_ID is selected this operation that hype is shown.

hypes.py keeps all the functions for the HYPES, COMMENTS and TAGS tables:
.. figure:: /static/29_init_drop_hypes.png
Initialize_Hypes() function creates the HYPES table if it is not initialized. In this table HYPE_ID is the primary key and is generated automatically with the SERIAL keyword. USER_ID refers to the USERS table and stores which user has submitted the hype.
Drop_Hypes() function drops the table HYPES.
.. figure:: /static/28_init_drop_comments.png
Initialize_Comments() function creates the COMMENTS table if it is not initialized. In this table COMMENT_ID is the primary key and is generated automatically with the SERIAL keyword. HYPE_ID refers to the HYPES table and stores which hype was commented.
Drop_Comments() function drops the table COMMENTS.
.. figure:: /static/30_init_drop_tags.png
Initialize_Tags() function creates the TAGS table if it is not initialized. In this table TAG_ID is the primary key and is generated automatically with the SERIAL keyword. HYPE_ID refers to the HYPES table and stores which hype this tag was added.
Drop_Tags() function drops the table TAGS.
.. figure:: /static/19_add_hype.png
Add_Hype() takes the required information as variables then adds a new entry to the HYPES table using these variables.
.. figure:: /static/25_get_hype_id.png
Get_Hype_ID() selects the hype with the given HYPE_ID and returns it.
.. figure:: /static/31_select_all_hypes.png
Select_All_Hypes() selects all the hypes in the HYPES table and returns it.
.. figure:: /static/21_comment_hype.png
Comment_Hype() takes the required information as variables then adds a new entry to the COMMENTS table using these variables.
.. figure:: /static/20_add_tags.png
Add_Tags() takes the required information as variables then adds a new entry to the TAGS table using these variables.

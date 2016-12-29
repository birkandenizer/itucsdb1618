Parts Implemented by Utku Öner
================================
For every User
~~~~~~~~~~~~~~~~~~
Signup/Login Page
------------------
This page handles the signup and login actions. Users can login via the form on the right and signup via the form on the left. If a user enters wrong credentials for the login form, the user will be redirected to the failed login error page.

.. figure:: /static/insert_operation_Users.png
   :scale: 50 %
   :alt: Signup/Login page

   Screenshot of the Signup/Login page.

Account Page
------------------
The account page is where that specific user's hypes and avatar is displayed. There is also a follow button in order for the viewing user to follow that the viewed user.

.. figure:: /static/account.png
   :scale: 50 %
   :alt: Account page

   Screenshot of the Account page of user onerut.


Hypeline Page
------------------
The hypeline is the main feature of the site. This page is only viewable if the user is logged in. This page will display the hypes that the user sent and the hypes from users that the user follows. The hypes have buttons which perform the respective operations. The user will also be redirected to this page when he/she tries to visit the home page while logged in.

.. figure:: /static/Hypeline.png
   :scale: 50 %
   :alt: Hypeline page

   Screenshot of the Hypeline page.


Errors
------------------

**Failed Login**

This page will be shown if wrong credentials are entered into the login form. The user has to then go back to the login screen and try again.

.. figure:: /static/failedlogin.png
   :scale: 50 %
   :alt: Failed Login

   Screenshot of the failed login error.

**Permission Error**

This page will be shown if a user tries to access management pages without administrator access.

.. figure:: /static/permission.png
   :scale: 50 %
   :alt: Permission

   Screenshot of the permission error.

For Administrators
~~~~~~~~~~~~~~~~~~
The following pages are for **administrators only**. They are implemented in order to provide a GUI to the administrators. These pages allow access to the database via the insert, update and delete operations. Administrators can use these to alter any data as required. These pages are off limits to any other user since the site will perform a role check before entering these pages and redirect the user to an error page if it fails.

User Management Page
------------------
This page allows access to the USERS table, by visiting "/userManagement". The two forms located on the page will allow the update and delete operations, in order to use the insert operation the signup page must be utilized. The page also lists the entries in the USERS table.

.. figure:: /static/delete_update_select_operation_Users.png
   :scale: 50 %
   :alt: User Management

   Screenshot of the User Management page.

Role Management Page
------------------
This page allows access to the ROLES table, by visiting "/roleManagement". The two forms located on the page will allow the insert, update and delete operations. The page also lists the entries in the ROLES table.

.. figure:: /static/Screenshot_roles.png
   :scale: 50 %
   :alt: Role Management

   Screenshot of the Role Management page.

Hypeblock Management Page
------------------
This page allows access to the HYPEBLOCKS table, by visiting "/hypeblockManagement". The two forms located on the page will allow the insert, update and delete operations. The page also lists the entries in the HYPEBLOCKS table.

.. figure:: /static/hypeblock.png
   :scale: 50 %
   :alt: Hypeblock Management

   Screenshot of the Hypeblock Management page.



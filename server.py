import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask.helpers import url_for

from attachment import Attachment
from contacts import Contact
from block import block
from favorite import Favorite
from followers import followers
from hypeline import Hypeline
from picture import Picture
from rehype import Rehype
from role import Role
from trending import Trending
from user import User
from hypeblock import Hypeblock
from dislike import dislike
from hypes import Hype

app = Flask(__name__)
app.attachment=Attachment(app)
app.block=block(app)
app.contacts=Contact(app)
app.favorite=Favorite(app)
app.followers=followers(app)
app.hypeline=Hypeline(app)
app.picture=Picture(app)
app.rehype=Rehype(app)
app.role=Role(app)
app.trending=Trending(app)
app.user=User(app)
app.hypeblock=Hypeblock(app)
app.dislike=dislike(app)
app.hype=Hype(app)


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS USERS (
        USER_ID        SERIAL PRIMARY KEY NOT NULL,
        USERNAME       VARCHAR(50) UNIQUE NOT NULL,
        NAME           VARCHAR(50) NOT NULL,
        SURNAME        VARCHAR(50) NOT NULL,
        EMAIL          VARCHAR(50) NOT NULL,
        PASSWORD       VARCHAR(25) NOT NULL,
        FOLLOWERCOUNT  INT
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS ROLES (
        ID             SERIAL PRIMARY KEY,
        USER_ID        INT REFERENCES USERS(USER_ID) ON DELETE CASCADE,
        TAG            VARCHAR(50) NOT NULL,
        TYPE           VARCHAR(50) NOT NULL
        )"""
        cursor.execute(query)

        query = """ CREATE TABLE IF NOT EXISTS FOLLOWER(
        PERSON_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
        FOLLOWER_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
        GROUP_NAME VARCHAR(50),
        DATE DATE NOT NULL,
        PRIMARY KEY(PERSON_ID,FOLLOWER_ID)
        )"""
        cursor.execute(query)

        query = """ CREATE TABLE IF NOT EXISTS BLOCKED(
        PERSON_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
        BLOCK_ID INTEGER NOT NULL REFERENCES USERS (USER_ID) ON DELETE CASCADE,
        REASON VARCHAR(50),
        DATE DATE NOT NULL,
        PRIMARY KEY(PERSON_ID,BLOCK_ID)
        )"""
        cursor.execute(query)
        
        connection.commit()
        
        app.hype.Initialize_Hypes()
        app.hypeblock.initialize_table()
        app.attachment.initialize_table()
        app.contacts.initialize_table()
        app.picture.initialize_table()
        app.rehype.initialize_Rehype()
        app.favorite.initialize_Favorite()
        app.trending.initialize_Trending()
        app.hype.Initialize_Comments()
        app.hype.Initialize_Tags()

    return redirect(url_for('home_page'))

@app.route('/dropitucsdb1618')
def drop_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS ROLES"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS COMMENTS"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS FOLLOWER"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS BLOCKED"""
        cursor.execute(query)

        connection.commit()
        
        app.hypeblock.drop_table()
        app.attachment.drop_table()
        app.contacts.drop_table()
        app.picture.drop_table()
        app.favorite.drop_Favorite()
        app.rehype.drop_Rehype()
        app.trending.drop_Trending()
        app.hype.Drop_Comments()
        app.hype.Drop_Hypes()
        app.hype.Drop_Tags()

        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS USERS"""
        cursor.execute(query)

        connection.commit()
        
        initialize_database()

    return redirect(url_for('home_page'))

@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count

@app.route('/addUser', methods=['POST'])
def add_user():
    username = request.form['username']
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = request.form['password']
    #retype = request.form('retype')
    app.user.Add_Users(username, name, surname, email, password)
    user_id=app.user.Get_User(username)
    user_id = user_id[0][0]
    return render_template("picture.html", user_id = user_id)

@app.route('/updateUser', methods=['POST'])
def update_user():
    pick = request.form['pick']
    username = request.form['username']
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = request.form['password']

    app.user.Update_Users(pick, username, name, surname, email, password)
    return redirect(url_for('user_management_page'))

@app.route('/deleteUser', methods=['POST'])
def delete_user():
    pick = request.form['pick']
    app.user.Delete_Users(pick)
    return redirect(url_for('user_management_page'))

@app.route('/userManagement')
def user_management_page():
    return render_template('users.html', users = app.user.List_Users())

@app.route('/roleManagement')
def roles_page():
    return render_template('roles.html', roles = app.role.List_Roles(), users = app.user.List_Users())

@app.route('/addRole', methods=['POST'])
def add_role():
    userid = request.form['userid']
    tag = request.form['tag']
    type = request.form['type']
    app.role.Add_Roles(userid, tag, type)
    return redirect(url_for('roles_page'))

@app.route('/updateRole', methods=['POST'])
def update_role():
    id = request.form['id']
    tag = request.form['tag']
    type = request.form['type']
    app.role.Update_Roles(id, tag, type)
    return redirect(url_for('roles_page'))

@app.route('/deleteRole', methods=['POST'])
def delete_role():
    id = request.form['id']
    app.role.Delete_Roles(id)
    return redirect(url_for('roles_page'))

@app.route('/hypeblockManagement')
def hypeblock_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        try:
            cursor = connection.cursor()
            query = """ SELECT * FROM HYPES ORDER BY HYPE_ID"""
            cursor.execute(query)
            hypes = cursor.fetchall()
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            connection.commit()
    return render_template('hypeblock.html', hypeblocks = app.hypeblock.List_BlockedHypes(), users = app.user.List_Users(), hypes = hypes)

@app.route('/addhypeblock', methods=['POST'])
def add_hypeblock():
    id = request.form['userid']
    hypeid = request.form['hypeid']
    reason = request.form['reason']
    personal = request.form['personal']
    app.hypeblock.Add_BlockedHypes(id, hypeid, reason, personal)
    return redirect(url_for('hypeblock_page'))

@app.route('/updatehypeblock', methods=['POST'])
def update_hypeblock():
    id = request.form['id']
    hypeid = request.form['hypeid']
    reason = request.form['reason']
    personal = request.form['personal']
    app.hypeblock.Update_BlockedHypes(id, hypeid, reason, personal)
    return redirect(url_for('hypeblock_page'))

@app.route('/deletehypeblock', methods=['POST'])
def delete_hypeblock():
    id = request.form['id']
    app.hypeblock.Delete_BlockedHypes(id)
    return redirect(url_for('hypeblock_page'))

@app.route('/hypeline')
def hypeline_page():
    return render_template('hypeline.html', hypes = app.hypeline.List_Hypes())

@app.route('/news')
def news_page():
    return render_template('news.html')


@app.route('/sport', methods=['GET', 'POST'])
def sport_page():
    if request.method == 'GET':
        return render_template('sport.html' , sportpage = app.followers.select_followers() , sportuser = app.followers.select_users())
    else:
        person_id = request.form['person_id']
        follower_id = request.form['follower_id']
        group_name = request.form['group_name']
        app.followers.update_group(person_id, follower_id, group_name)
        return render_template('show_users_following.html' , sportpage2 = app.followers.show_followers())


@app.route('/sport_block_update', methods=['GET', 'POST'])
def sport_page_block_uptade():
    if request.method == 'GET':
        return render_template('show_users_blocked.html' , sportuser2 = app.block.select_users())
    else:
        person_id = request.form['person_id']
        block_id = request.form['block_id']
        reason = request.form['reason']
        app.block.update_reason(person_id, block_id, reason)
        return render_template('show_users_blocked.html' , sportuser2 = app.block.select_users())

@app.route('/sport_block', methods=['GET', 'POST'])
def sport_page_add_x():
    if request.method == 'GET':
        return render_template('sport.html' , sportpage = app.followers.select_followers() , sportuser = app.followers.select_users())
    else:
        person_id = request.form['user_ids']
        block_id = request.form['user_blocked']
        reason = request.form['reason']
        app.block.add_block(person_id, block_id, reason)
        return render_template('show_users_blocked.html' , sportuser2 = app.block.select_users())

@app.route('/sport/unblock/<person_id>/<block_id>')
def sport_page_unblock(person_id, block_id):
    app.block.delete_block(person_id, block_id)
    return render_template('sport.html' , sportpage = app.followers.select_followers() , sportuser = app.followers.select_users())


@app.route('/sport/add/<follower_id>')
def sport_page_add(follower_id):
    sayi=2
    app.followers.add_follow(sayi, follower_id)
    return render_template('show_users_following.html' , sportpage2 = app.followers.show_followers())


@app.route('/sport/delete/<follower_id>')
def sport_page_delete(follower_id):
    app.followers.delete_follow(follower_id)
    return render_template('show_users_following.html' , sportpage2 = app.followers.show_followers())


@app.route('/technology')
def technology_page():
    return render_template('technology.html')

@app.route('/music')
def music_page():
    hypespage = app.rehype.List_Hypes()
    hypespageUsername = app.rehype.List_Users()
    trending = app.trending.List_Trending()
    return render_template('music.html', hypespage = hypespage, hypespageUsername = hypespageUsername, trending=trending)

@app.route('/trending/<hype_id>')
def music_page_trending(hype_id):
    hypespage = app.trending.List_Trending_Hypes(hype_id)
    hypespageUsername = app.rehype.List_Users()
    trending = app.trending.List_Trending()
    return render_template('music.html', hypespage = hypespage, hypespageUsername = hypespageUsername, trending=trending)

@app.route('/reypeslist')
def rehypes_list():
    rehypespage = app.rehype.List_Rehypes()
    rehypesUser = app.rehype.List_Users()
    return render_template('rehypes_list.html', rehypespage = rehypespage, rehypesUser = rehypesUser)

@app.route('/rehypes', methods=['GET', 'POST'])
def rehypes_page():
    if request.method == 'GET':
        rehypesUser = app.rehype.List_Users()
        return render_template('rehypes.html', rehypespage = app.rehype.List_Rehypes(), rehypesUser = rehypesUser)
    else:
        comment = request.form['comment']
        old_user_id = request.form['old_user_id']
        hype_id = request.form['hype_id']
        user_ids = request.form['user_ids']
        app.rehype.Update_Rehype(old_user_id, hype_id, comment, user_ids)
        element = app.trending.Decision_Add(hype_id)
        if element != 0:
            app.trending.Add_Trending(element[0],element[1], element[2])
        element = False
        element = app.trending.Decision_Update_Add(hype_id)
        if element == True:
            app.trending.Update_Trending(hype_id, 1)
        rehypesUser = app.rehype.List_Users()
        return render_template('rehypes_list.html', rehypespage = app.rehype.List_Rehypes(), rehypesUser = rehypesUser)

@app.route('/music/add/<user_id>/<hype_id>')
def music_page_add(user_id, hype_id):
    app.rehype.Add_Rehype(user_id, hype_id)
    rehypesUser = app.rehype.List_Users()
    return render_template('rehypes.html', rehypespage = app.rehype.List_Rehypes(), rehypesUser = rehypesUser)

@app.route('/music/delete/<user_id>/<hype_id>')
def music_page_delete(user_id, hype_id):
    hype_ids = app.rehype.Delete_Rehype(user_id, hype_id)
    element = False
    element = app.trending.Decision_Delete(hype_ids)
    if element == True:
        app.trending.Delete_Trending(hype_ids)
    element = False
    element = app.trending.Decision_Update_Del(hype_ids)
    if element == True:
        app.trending.Update_Trending(hype_ids, 2)
    rehypesUser = app.rehype.List_Users()
    return render_template('rehypes_list.html', rehypespage = app.rehype.List_Rehypes(), rehypesUser = rehypesUser)


@app.route('/favorites', methods=['GET','POST'])
def favorites_select():
    if request.method =='GET':
        hypespageUsername = app.rehype.List_Users()
        return render_template('favorites.html', hypespageUsername=hypespageUsername)
    else:
        user_ids = request.form['user_ids']
        favorites = app.favorite.List_Favorites(user_ids)
        rehypesUser = app.rehype.List_Users()
        return render_template('selectedfavorites.html', favorites=favorites, rehypesUser=rehypesUser)

@app.route('/favorite/del/<favorite_id>')
def favorite_delete(favorite_id):
    app.favorite.Delete_Favorite(favorite_id)
    hypespageUsername = app.rehype.List_Users()
    return render_template('favorites.html', hypespageUsername=hypespageUsername)

@app.route('/favorite/update/<favorite_id>', methods=['GET','POST'])
def favorite_update(favorite_id):
    if request.method == 'GET':
        favorites=app.favorite.List_FavoritesID(favorite_id)
        return render_template('favorite_update.html', favorites=favorites)
    else:
        favorite_id = request.form['favorite_id']
        rate = request.form['rate']
        app.favorite.Update_Favorite(favorite_id, rate)
        hypespageUsername = app.rehype.List_Users()
        return render_template('favorites.html', hypespageUsername=hypespageUsername)

@app.route('/favoriteadd', methods=['GET','POST'])
def favorite_add():
    if request.method == 'GET':
        hypespageUsername = app.rehype.List_Users()
        return render_template('music.html', hypespage = app.rehype.List_Hypes(), hypespageUsername = hypespageUsername)
    else:
        hype_id = request.form['hype_id']
        user_ids = request.form['user3_ids']
        app.favorite.Add_Favorite(user_ids, hype_id)
        hypespageUsername = app.rehype.List_Users()
        return render_template('music.html', hypespage = app.rehype.List_Hypes(), hypespageUsername = hypespageUsername)

@app.route('/dislikes', methods=['GET','POST'])
def dislikes_select():
    if request.method =='GET':
        return render_template('dislikes.html', hypes = app.dislike.List_Hypes(), users = app.dislike.select_users())
    else:
        user_ids = request.form['user_ids']
        dislikes = app.dislike.List_Dislikes(user_ids)
        rehypesUser = app.rehype.List_Users()
        return render_template('selecteddislikes.html', dislikes=dislikes, rehypesUser=rehypesUser)

@app.route('/dislike_cancel/<hype_id>/<user_id>')
def dislike_cancel(hype_id, user_id):
    app.dislike.delete_dislike(hype_id, user_id)
    return render_template('dislikes_selected.html' , users_dislike = app.dislike.select_dislikes())

@app.route('/dislike_reason_update', methods=['GET', 'POST'])
def dislike_reason_update_func():
    if request.method == 'GET':
        return render_template('dislikes_selected.html' , users_dislike = app.dislike.select_dislikes())
    else:
        hype_id = request.form['hype_id']
        user_id = request.form['user_id']
        reason = request.form['reason']
        app.dislike.update_reason(hype_id, user_id, reason)
        return render_template('dislikes_selected.html' , users_dislike = app.dislike.select_dislikes())

@app.route('/dislike_add', methods=['GET', 'POST'])
def dislike_adds():
    if request.method == 'GET':
        return render_template('dislikes.html', hypes = app.dislike.List_Hypes(), users = app.dislike.select_users())
    else:
        hype_id = request.form['hype_dislike']
        user_id = request.form['user_ids']
        reason = request.form['reason']
        app.dislike.add_dislike(user_id, hype_id, reason)
        return render_template('dislikes_selected.html',users_dislike = app.dislike.select_dislikes())    
    
@app.route('/events')
def events_page():
    return render_template('events.html')
@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/contact')
def contact_page():
    return render_template('contact.html')
@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html', contacts = app.contacts.list_contacts())

@app.route('/contact/add',methods=['POST'])
def add_contact():
    with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT TICKET_ID FROM CONTACT ORDER BY TICKET_ID DESC LIMIT 1"
            cursor.execute(query)
            ticket_id = cursor.fetchone()
            if  ticket_id is None:
                ticket_id = 1
            else:
                ticket_id = ticket_id[0]
                ticket_id = ticket_id + 1
            subject = request.form['subject']
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            message = request.form['message']
    app.contacts.add_contact(ticket_id,subject,name,surname,email,message)
    return redirect(url_for('home_page'))

@app.route('/contact/update/<ticket_id>', methods=['GET', 'POST'])
def update_contact(ticket_id):
    if request.method == 'GET':
        return render_template('contact_update.html', ticket_id = ticket_id)
    else:
        ticket_id = request.form['ticket_id']
        subject = request.form['subject']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        message = request.form['message']
        app.contacts.update_contact(subject,name,surname,email,message,ticket_id)
        return redirect(url_for('contacts_page'))

@app.route('/contact/delete/<ticket_id>')
def delete_contact(ticket_id):
    app.contacts.delete_contact(ticket_id)
    return redirect(url_for('contacts_page'))

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/hype')
def hype_page():
    hypes=app.hype.Select_All_Hypes()
    return render_template('hype.html', hypes = hypes)

@app.route('/addHype', methods=['POST'])
def hype():
    user_id = request.form['user_id']
    t = datetime.date.today()
    text = request.form['hype_text']
    topic = request.form['topic']

    app.hype.Add_Hype(user_id, t, text, topic)
    hype_id=app.hype.Get_Hype_ID(user_id, t, text, topic)
    app.hype.Add_Tags(hype_id, t, tags)

    return render_template("attachment.html", hype_id=hype_id)

@app.route('/commentHype', methods=['POST'])
def comment_hype():
    hype_id = request.form['comment_hype_id']
    user_id = request.form['comment_user_id']
    t = datetime.date.today()
    text = request.form['comment_text']
    app.hype.Comment_Hype(hype_id, user_id, t, text)

    return redirect(url_for('hype_page'))

@app.route('/editHype', methods=['POST'])
def edit_hype():
    with dbapi2.connect(app.config['dsn']) as connection:
        hype_id = request.form['update_hype_id']
        text = request.form['update_hype_text']
        cursor = connection.cursor()
        query = "UPDATE HYPES SET TEXT = '"+ text +"' WHERE HYPE_ID =" + str(hype_id)
        cursor.execute(query)

    return redirect(url_for('hype_page'))

@app.route('/deleteHype', methods=['POST'])
def delete_hype():
    with dbapi2.connect(app.config['dsn']) as connection:
        hype_id = request.form['delete_hype_id']
        cursor = connection.cursor()
        query = "DELETE FROM HYPES WHERE HYPE_ID =" + str(hype_id)
        cursor.execute(query)
    return redirect(url_for('hype_page'))

@app.route('/selectHype', methods=['POST'])
def select_hype():
    with dbapi2.connect(app.config['dsn']) as connection:
        hype_id = request.form['select_hype_id']
        cursor = connection.cursor()
        query = "SELECT * FROM HYPES WHERE HYPE_ID =" + str(hype_id)
        cursor.execute(query)
        selectedHype = cursor.fetchall()
    return redirect(url_for('hype_page'))

@app.route('/hype/attachment')
def attachment_page():
    return render_template('attachment.html')

@app.route('/hype/attachment/add',methods=['POST'])
def add_attachment():
    with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT ATTACHMENT_ID FROM ATTACHMENT ORDER BY ATTACHMENT_ID DESC LIMIT 1"
            cursor.execute(query)
            attachment_id = cursor.fetchone()
            if  attachment_id is None:
                attachment_id = 1
            else:
                attachment_id = attachment_id[0]
                attachment_id = attachment_id + 1

            hype_id = request.form['hype_id']
            attachment_type = request.form['attachment_type']
            url = request.form['url']

    app.attachment.add_attachment(attachment_id,hype_id,attachment_type,url)
    return redirect(url_for('list_attachment'))

@app.route('/hype/attachment/list',methods=['GET'])
def list_attachment():
    return render_template('attachments.html',attachmentspage = app.attachment.list_attachments())

@app.route('/hype/attachment/update/<attachment_id>',methods=['GET', 'POST'])
def update_attachment(attachment_id):
    if request.method == 'GET':
        return render_template('attachment_update.html', attachment_id = attachment_id)

    else:
        attachment_id=request.form['attachment_id']
        attachment_type=request.form['attachment_type']
        url=request.form['url']
        app.attachment.update_attachment(attachment_id,attachment_type,url)
        return redirect(url_for('list_attachment'))

@app.route('/hype/attachment/delete/<attachment_id>')
def delete_attachment(attachment_id):
    app.attachment.delete_attachment(attachment_id)
    return render_template('attachments.html' , attachmentspage = app.attachment.list_attachments())

@app.route('/user/picture')
def picture_page():
    return render_template('picture.html')

@app.route('/user/picture/add',methods=['POST'])
def add_picture():
    with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT PICTURE_ID FROM PICTURE ORDER BY PICTURE_ID DESC LIMIT 1"
            cursor.execute(query)
            picture_id = cursor.fetchone()
            if  picture_id is None:
                picture_id = 1
            else:
                picture_id = picture_id[0]
                picture_id = picture_id + 1

            user_id = request.form['user_id']
            url = request.form['url']

    app.picture.add_picture(picture_id,user_id,url)
    return redirect(url_for('list_picture'))

@app.route('/user/picture/list',methods=['GET'])
def list_picture():
    return render_template('pictures.html',picturespage = app.picture.list_pictures())

@app.route('/user/picture/update/<picture_id>',methods=['GET', 'POST'])
def update_picture(picture_id):
    if request.method == 'GET':
        return render_template('picture_update.html', picture_id = picture_id)

    else:
        attachment_id=request.form['attachment_id']
        url=request.form['url']
        app.picture.update_picture(picture_id,url)
        return redirect(url_for('list_picture'))

@app.route('/user/picture/delete/<picture_id>')
def delete_picture(picture_id):
    app.picture.delete_picture(picture_id)
    return render_template('pictures.html' , picturespage = app.picture.list_pictures())

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb1618'"""

    app.run(host='0.0.0.0', port=port, debug=debug)

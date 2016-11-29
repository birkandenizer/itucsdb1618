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

from rehype import Rehype
from favorite import Favorite
from contact import contact
from contacts import store_contact
from followers import followers

app = Flask(__name__)
app.rehype=Rehype(app)
app.favorite=Favorite(app)
app.store_contact = store_contact(app)
app.followers = followers(app)

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
        USER_ID        INT PRIMARY KEY NOT NULL,
        USERNAME       VARCHAR(50) NOT NULL,
        NAME           VARCHAR(50) NOT NULL,
        SURNAME        VARCHAR(50) NOT NULL,
        EMAIL          VARCHAR(50) NOT NULL,
        PASSWORD       VARCHAR(25) NOT NULL,
        FOLLOWERCOUNT  INT
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS CONTACT (
        SUBJECT     VARCHAR(20) NOT NULL,
        NAME        VARCHAR(20) NOT NULL,
        SURNAME     VARCHAR(20) NOT NULL,
        EMAIL       VARCHAR(30) NOT NULL,
        MESSAGE   VARCHAR(200) NOT NULL,
        TICKET_ID    INT PRIMARY KEY NOT NULL
        )"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS HYPES"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS HYPES (
        HYPE_ID         INT             PRIMARY KEY     NOT NULL,
        USER_ID         INT                             NOT NULL,
        DATE            DATE                            NOT NULL,
        TEXT            VARCHAR(150)                    NOT NULL,
        TOPIC           VARCHAR(20)                     NOT NULL
        )"""
        cursor.execute(query)

        query = """INSERT INTO HYPES (
        HYPE_ID,
        USER_ID,
        DATE,
        TEXT,
        TOPIC)
        VALUES (152, 15, '2016-10-30', 'OMG!! MacBook Pro 2016 was released this week! It is even prettier than my girlfriend :)', 'Technology')"""
        cursor.execute(query)

        query = """ DROP TABLE IF EXISTS REHYPES """
        cursor.execute(query)

        query = """ CREATE TABLE IF NOT EXISTS REHYPES(
        HYPE_ID INTEGER NOT NULL,
        USER_ID INTEGER NOT NULL,
        COMMENT VARCHAR(200),
        DATE DATE NOT NULL,
        PRIMARY KEY (HYPE_ID, USER_ID)
        )"""
        cursor.execute(query)

        query = """ DROP TABLE IF EXISTS FAVORITES """
        cursor.execute(query)

        query = """ CREATE TABLE IF NOT EXISTS FAVORITES(
        ID SERIAL PRIMARY KEY,
        HYPE_ID INTEGER NOT NULL,
        USER_ID INTEGER NOT NULL,
        DATE DATE NOT NULL,
        RATE INTEGER NOT NULL,
        UNIQUE(HYPE_ID,USER_ID)
        )"""
        cursor.execute(query)


        query = """ DROP TABLE IF EXISTS FOLLOWER """
        cursor.execute(query)

        query = """ CREATE TABLE IF NOT EXISTS FOLLOWER(
        PERSON_ID INTEGER NOT NULL,
        FOLLOWER_ID INTEGER NOT NULL,
        GROUP_NAME VARCHAR(50),
        DATE DATE NOT NULL,
        PRIMARY KEY(PERSON_ID,FOLLOWER_ID)
        )"""
        cursor.execute(query)

        query = """INSERT INTO FOLLOWER(PERSON_ID, FOLLOWER_ID, GROUP_NAME, DATE) VALUES (1, 2, 'Family' , '2016-10-31')"""
        cursor.execute(query)


        connection.commit()

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
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "SELECT USER_ID FROM USERS ORDER BY USER_ID DESC LIMIT 1"
        cursor.execute(query)
        userid = cursor.fetchone()
        if userid is None:
            userid = 1
        else:
            userid = userid[0]
            userid = userid + 1

    username = request.form['username']
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = request.form['password']
    #retype = request.form('retype')

    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO USERS (
        USER_ID,
        USERNAME,
        NAME,
        SURNAME,
        EMAIL,
        PASSWORD,
        FOLLOWERCOUNT)
        VALUES ("""+ str(userid)  +""", '"""+ username  +"""', '"""+ name +"""', '"""+ surname +"""', '"""+ email +"""', '"""+ password +"""', 0)"""
        cursor.execute(query)

    return redirect(url_for('home_page'))

@app.route('/updateUser', methods=['POST'])
def update_user():
    pick = request.form['pick']
    username = request.form['username']
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = request.form['password']
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "SELECT USER_ID FROM USERS WHERE USERNAME = '" + pick + "'"
        cursor.execute(query)
        tmp = cursor.fetchone()
        if tmp is not None:
            query = """UPDATE USERS
            SET USERNAME = '"""+ username +"""', NAME = '"""+ name +"""',
            SURNAME = '"""+ surname +"""', EMAIL = '"""+ email +"""',
            PASSWORD = '"""+ password +"""'
            WHERE USERNAME = '""" + pick +"""'"""
            cursor.execute(query)
    return redirect(url_for('user_management_page'))

@app.route('/deleteUser', methods=['POST'])
def delete_user():
    pick = request.form['pick']
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "SELECT USER_ID FROM USERS WHERE USERNAME = '" + pick + "'"
        cursor.execute(query)
        tmp = cursor.fetchone()
        if tmp is not None:
            query = "DELETE FROM USERS WHERE USERNAME = '" + pick + "'"
            cursor.execute(query)
    return redirect(url_for('user_management_page'))

@app.route('/userManagement')
def user_management_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        try:
            cursor = connection.cursor()
            query = """ SELECT * FROM USERS ORDER BY USER_ID"""
            cursor.execute(query)
            users = cursor.fetchall()
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            connection.commit()
    return render_template('users.html', users = users)

@app.route('/news')
def news_page():
    return render_template('news.html')


@app.route('/sport', methods=['GET', 'POST'])
def sport_page():
    if request.method == 'GET':
        return render_template('sport.html' , sportpage = app.followers.select_followers())
    else:
        person_id = request.form['person_id']
        follower_id = request.form['follower_id']
        group_name = request.form['group_name']
        app.followers.update_group(person_id, follower_id, group_name)
        return render_template('sport.html' , sportpage = app.followers.select_followers())



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
    return render_template('music.html', hypespage = hypespage, hypespageUsername = hypespageUsername)

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
        rehypesUser = app.rehype.List_Users()
        return render_template('rehypes_list.html', rehypespage = app.rehype.List_Rehypes(), rehypesUser = rehypesUser)

@app.route('/music/add/<user_id>/<hype_id>')
def music_page_add(user_id, hype_id):
    app.rehype.Add_Rehype(user_id, hype_id)
    rehypesUser = app.rehype.List_Users()
    return render_template('rehypes.html', rehypespage = app.rehype.List_Rehypes(), rehypesUser = rehypesUser)

@app.route('/music/delete/<user_id>')
def music_page_delete(user_id):
    app.rehype.Delete_Rehype(user_id)
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
    return render_template('contacts.html', contacts = app.store_contact.select_contact())

@app.route('/contact/add',methods=['POST'])
def contact_add_page():
    subject = request.form['subject']
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    message = request.form['message']
    ticket_id = request.form['ticket_id']
    with dbapi2.connect(app.config['dsn']) as connection:
        try:
            cursor = connection.cursor()
            query = """INSERT INTO CONTACT (SUBJECT,NAME,SURNAME,EMAIL,MESSAGE,TICKET_ID)
            VALUES ('"""+ subject  +"""', '"""+ name  +"""', '"""+ surname +"""', '"""+ email +"""', '"""+ message +"""','"""+ ticket_id +"""')"""
            cursor.execute(query)
        except dbapi2.DatabaseError:
                connection.rollback()
        finally:
               connection.commit()
    return redirect(url_for('home_page'))


@app.route('/contact/update/<ticket_id>', methods=['GET', 'POST'])
def contact_update_page(ticket_id):
    if request.method == 'GET':
        return render_template('contact_update.html', contact = app.store_contact.get_contact(ticket_id))
    else:
        subject = request.form['subject']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        message = request.form['message']
        ticket_id = request.form['ticket_id']

        with dbapi2.connect(app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """UPDATE CONTACT
                 SET SUBJECT = '"""+ subject +"""', NAME = '"""+ name +"""',
                 SURNAME = '"""+ surname +"""', EMAIL = '"""+ email +"""',
                 MESSAGE = '"""+ message +"""'
                 WHERE TICKET_ID = '""" + ticket_id +"""'"""
                cursor.execute(query, (subject, name, surname, email, message, ticket_id))
                connection.commit()
                cursor.close()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
        return redirect(url_for('contacts_page'))

@app.route('/contact/delete/<ticket_id>', methods=['GET', 'POST'])
def contact_delete_page(ticket_id):
    if request.method == 'GET':
        return render_template('contact_delete.html', contact = app.store_contact.delete_contact(ticket_id))
    else:
        ticket_id = request.form['ticket_id']

        with dbapi2.connect(app.config['dsn']) as connection:
            try:
                cursor = connection.cursor()
                query = """ DELETE FROM CONTACT WHERE ticket_id = %s """
                cursor.execute(query, [ticket_id])
                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
            finally:
               connection.commit()
        return redirect(url_for('contacts_page'))
@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/hype')
def hype_page():
    return render_template('hype.html')

@app.route('/addHype', methods=['POST'])
def hype():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = "SELECT HYPE_ID FROM HYPES ORDER BY HYPE_ID DESC LIMIT 1"
        cursor.execute(query)
        hype_id = cursor.fetchone()
        if hype_id is None:
            hype_id = 1
        else:
            hype_id = hype_id[0]
            hype_id = hype_id + 1

    user_id = request.form['user_id']
    t = datetime.date.today()
    text = request.form['hype_text']
    topic = request.form['topic']

    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """INSERT INTO HYPES(
        HYPE_ID,
        USER_ID,
        DATE,
        TEXT,
        TOPIC)
        VALUES("""+ str(hype_id) +", "+ str(user_id) +",'" + str(t) +"','"+ text +"','"+ topic +"' )"
        cursor.execute(query)

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
    return render_template('hype.html', hypes = selectedHype)

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

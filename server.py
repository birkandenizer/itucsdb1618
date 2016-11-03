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
from contact import contact
from contacts import store_contact

app = Flask(__name__)
app.rehype=Rehype(app)
app.store_contact = store_contact(app)

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

        query = """INSERT INTO REHYPES(
        HYPE_ID,
        USER_ID,
        COMMENT,
        DATE)
        VALUES(152, 1, 'it is really great!', '2016-10-30')
        """
        cursor.execute(query)

        query = """INSERT INTO HYPES (
        HYPE_ID,
        USER_ID,
        DATE,
        TEXT,
        TOPIC)
        VALUES (92, 2, '2016-10-31', 'OMG!! MacBook Pro 2016 was released this week! It is even prettier than my girlfriend :)', 'Music')"""
        cursor.execute(query)

        query = """INSERT INTO HYPES (
        HYPE_ID,
        USER_ID,
        DATE,
        TEXT,
        TOPIC)
        VALUES (67, 3, '2016-10-31', 'OMG!! MacBook Pro 2016 was released this week! It is even prettier than my girlfriend :)', 'Music')"""
        cursor.execute(query)

        query = """ DROP TABLE IF EXISTS FOLLOWER """
        cursor.execute(query)

        query = """ CREATE TABLE IF NOT EXISTS FOLLOWER(
        PERSON_ID INTEGER NOT NULL,
        FOLLOWER_ID INTEGER NOT NULL,
        DATE DATE NOT NULL )"""
        cursor.execute(query)

        query = """INSERT INTO FOLLOWER(PERSON_ID, FOLLOWER_ID, DATE) VALUES (1, 2, '2016-10-31')"""
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
    return render_template('users.html')
@app.route('/news')
def news_page():
    return render_template('news.html')
@app.route('/sport')
def sport_page():
    return render_template('sport.html')
@app.route('/technology')
def technology_page():
    return render_template('technology.html')

@app.route('/music')
def music_page():
    return render_template('music.html', hypespage = app.rehype.List_Hypes())

@app.route('/rehypes', methods=['GET', 'POST'])
def rehypes_page():
    if request.method == 'GET':
        return render_template('rehypes.html', rehypespage = app.rehype.List_Rehypes())
    else:
        comment = request.form['comment']
        hype_id = request.form['hype_id']
        app.rehype.Update_Rehype(hype_id, comment)
        return render_template('rehypes.html', rehypespage = app.rehype.List_Rehypes())

@app.route('/music/add/<user_id>/<hype_id>')
def music_page_add(user_id, hype_id):
    app.rehype.Add_Rehype(user_id, hype_id)
    return render_template('rehypes.html', rehypespage = app.rehype.List_Rehypes())

@app.route('/music/delete/<user_id>')
def music_page_delete(user_id):
    app.rehype.Delete_Rehype(user_id)
    return render_template('rehypes.html', rehypespage = app.rehype.List_Rehypes())

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

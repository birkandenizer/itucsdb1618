import datetime
import json
import os
import psycopg2 as dbapi2
import re

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for


app = Flask(__name__)

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
        
        query = """DROP TABLE IF EXISTS USERS"""
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

        query = """INSERT INTO USERS (
        USER_ID,
        USERNAME,
        NAME,
        SURNAME,
        EMAIL,
        PASSWORD,
        FOLLOWERCOUNT)
        VALUES (1, 'onerut', 'Utku', 'Oner', 'onerut@itu.edu.tr', 'admin', 0)"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS CONTACT"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS CONTACT (TICKET_ID INT PRIMARY KEY NOT NULL, TOPIC VARCHAR(20) NOT NULL,
         NAME VARCHAR(20) NOT NULL, SURNAME VARCHAR(20) NOT NULL, USER_TEXT VARCHAR(200) NOT NULL, DATE INT NOT NULL)"""
        cursor.execute(query)

        query = """INSERT INTO CONTACT (TICKET_ID,TOPIC,NAME,SURNAME,USER_TEXT,DATE)
        VALUES (10,'LOGIN','BIRKAN','DENIZER','Houston we have a problem',2016)"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS HYPES"""
        cursor.execute(query)
        
        query = """CREATE TABLE IF NOT EXISTS HYPES (
        HYPE_ID         INT             PRIMARY KEY     NOT NULL,
        USER_ID         INT                             NOT NULL,
        DATE            INT                             NOT NULL,
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
        VALUES (152, 15, 2016, 'OMG!! MacBook Pro 2016 was released this week! It is even prettier than my girlfriend :)', 'Technology')"""
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
    return render_template('music.html')
@app.route('/events')
def events_page():
    return render_template('events.html')
@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/contact')
def contact_page():
    return render_template('contact.html')
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

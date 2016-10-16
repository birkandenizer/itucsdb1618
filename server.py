import datetime
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')


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
    app.run(host='0.0.0.0', port=port, debug=debug)

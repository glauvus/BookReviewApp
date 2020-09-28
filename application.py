import os, hashlib, binascii

from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
from models import *

app = Flask(__name__)

# Check if environment variable for database is set
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Load configuration
app.config.from_object("config.Config")

# Create session object and pass the application
Session(app)

# Initialize db
db.init_app(app)

"""
If user variable is set, i.e. user is logged in, returns the main page.
Else returns index page.
"""
@app.route("/")
def index():
    if 'user' in session:
        return render_template("main.html")
    return render_template("index.html")

"""
Retrieves the db record for the given username and converts key and salt to binary.
Hashes the given password and if it matches the retrieved one, 
sets the user variable and redirects to index().
"""
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    key = binascii.unhexlify(user.password)
    salt = binascii.unhexlify(user.salt)
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    if new_key == key:
        session['user'] = request.form['username']
        return redirect(url_for('index'))
    else:
        return render_template("index.html"), 401

"""
Sets a salt and hashes the given password.
Inserts a new record to the db with the given username and the hex values of key and salt.
Redirects to index().
"""
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    user = User(username=username, password=key.hex(), salt=salt.hex())
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

"""
Pops the user variable, i.e. logouts the user.
Redirects to index().
"""
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

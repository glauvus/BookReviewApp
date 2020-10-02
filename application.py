import os, hashlib, binascii, json, requests

from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
from sqlalchemy import or_
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
    if user is None:
        return render_template("index.html"), 401
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
    session.clear()
    return redirect(url_for('index'))

"""
Retrieves the db records that match the search text, and returns them in json format.
"""
@app.route("/<string:textToSearch>")
def search(textToSearch):
    books = Book.query.filter(or_(Book.isbn.like("%"+textToSearch+"%"), Book.title.like("%"+textToSearch+"%"), Book.author.like("%"+textToSearch+"%"))).all()
    return json.dumps([dict(isbn=b.isbn, title=b.title, author=b.author, year=b.year) for b in books])

"""
Sets the book session variable and retrieves the db record for the selected book and its reviews.
Requests number of ratings and average rating from goodreads.com API.
Returns book page.
"""
@app.route("/book-<string:isbn>")
def bookInfo(isbn):
    session['book'] = isbn
    book = Book.query.filter_by(isbn=isbn).first()
    reviews = db.session.query(Review, User).join(User).filter(Review.r_isbn==isbn).all()
    res = (requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "SH8qrv34ElgwVGpd4DvXg", "isbns": isbn})).json()
    ratingCount = res['books'][0]['work_ratings_count']
    avgRating = res['books'][0]['average_rating']
    return render_template("book.html", book=book, reviews=reviews, ratingCount=ratingCount, avgRating=avgRating)

"""
Inserts a new record to the db with book's isbn, user's username, review rating and comment.
Redirects to bookInfo(isbn).
"""
@app.route("/review", methods=["POST"])
def review():
    isbn = session['book']
    uid = (User.query.filter_by(username=session['user']).first()).uid
    reviewRating = request.form.get("reviewRating")
    reviewComment = request.form.get("reviewComment")
    review = Review(r_isbn=isbn, r_uid=uid, rating=reviewRating, comment=reviewComment)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('bookInfo', isbn=isbn))
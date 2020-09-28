from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)


class Review(db.Model):
    __tablename__ = "reviews"
    r_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), primary_key=True)
    r_uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)

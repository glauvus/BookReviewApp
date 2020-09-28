import os

class Config(object):
    SECRET_KEY = os.urandom(16)
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
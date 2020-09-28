import os

from flask import Flask, render_template
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


@app.route("/")
def index():
    return render_template("index.html")

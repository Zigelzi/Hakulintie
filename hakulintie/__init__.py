from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from hakulintie.forms import Rekisteroidy, Kirjaudu

# Initializing the app and the DB.
app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from hakulintie import routes
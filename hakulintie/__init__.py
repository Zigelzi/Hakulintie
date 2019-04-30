from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hakulintie.forms import Rekisteroidy, Kirjaudu
from hakulintie.config import Config, ProdConfig, DevConfig
from flask_bcrypt import Bcrypt

# Initializing the app and the DB.
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from hakulintie import routes
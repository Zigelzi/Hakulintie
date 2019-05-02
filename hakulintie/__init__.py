from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from hakulintie.config import Config, ProdConfig, DevConfig
from flask_bcrypt import Bcrypt

# Initializing the app and the DB.
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Initialize the login manager settings
login_manager = LoginManager(app)
login_manager.login_view = 'kirjaudu'
login_manager.login_message = 'Kirjaudu sisään päästäksesi tälle sivulle'


from hakulintie import routes


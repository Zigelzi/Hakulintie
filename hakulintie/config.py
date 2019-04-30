from os import environ

class Config(object):
    SECRET_KEY = environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
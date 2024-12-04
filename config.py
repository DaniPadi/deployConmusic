import os

basedir= os.path.abspath(os.path.dirname(__file__))

class config:
    SECRET_KEY= 'mysecretkey'
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    DEBUG= True
    pass

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Base de datos en memoria para pruebas
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


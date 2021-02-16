import os

path = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(path, '../flask_card.sqlite')
test_path = os.path.join(path, '../tests/test_db.sqlite')


class Config(object):
    NAME = 'Config'
    DEVELOPMENT = False
    TESTING = False
    SECRET_KEY = "temp_secret_key"


class DevelopmentConfig(Config):
    NAME = 'development'
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + database_path
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    NAME = 'testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + test_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False


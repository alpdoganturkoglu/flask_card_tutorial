import os


class Config(object):
    NAME = 'Config'
    DEVELOPMENT = False
    TESTING = False
    SECRET_KEY = "temp_secret_key"


class DevelopmentConfig(Config):
    NAME = 'development'
    DEVELOPMENT = True

    path = os.path.dirname(os.path.realpath(__file__))
    database_path = os.path.join(path, '../mydb.sqlite')
    DBPATH = database_path


class TestingConfig(Config):
    NAME = 'testing'
    TESTING = True

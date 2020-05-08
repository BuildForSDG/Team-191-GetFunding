import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]


class ProductionConfig(Config):
    ENV = "production"
    SECRET_KEY = os.environ["SECRET"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.environ["SECRET"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]


class TestingConfig(Config):
    TESTING = True

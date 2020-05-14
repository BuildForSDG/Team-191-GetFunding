import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]


class ProductionConfig(Config):
    ENV = "production"
    SECRET_KEY = os.environ["SECRET"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.environ["SECRET"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]


class TestingConfig(Config):
    TESTING = True
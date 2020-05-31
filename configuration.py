"""
configure the application using a python module called
decouple."""


from decouple import config



class MainConfig():
    DEBUG = False
    TESTING = False
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(MainConfig):
    DB_NAME = 'ProductionCreditScore'
    SQLALCHEMY_DATABASE_URI = config('PRODUCTION_URI')


class DevelopmentConfig(MainConfig):
    DEBUG = True
    DB_NAME = 'DevelopmentCreditScore'
    SQLALCHEMY_DATABASE_URI = config('DEVELOPMENT_URI')

class TestingConfig(MainConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = config('TESTING_URI')
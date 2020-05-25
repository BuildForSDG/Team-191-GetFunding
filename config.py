"""configure the application using a python module called
decouple."""


from decouple import config



class Config():
    DEBUG = False
    TESTING = False
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DB_NAME = 'ProductionCreditScore'
    SQLALCHEMY_DATABASE_URI = config('PRODUCTION_URI')


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = 'DevelopmentCreditScore'
    SQLALCHEMY_DATABASE_URI = config('DEVELOPMENT_URI')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = config('TESTING_URI')
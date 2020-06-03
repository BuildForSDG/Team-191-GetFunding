"""configure the application using a python module called
decouple."""


from decouple import config



class MainConfig():
    DEBUG = False
    TESTING = False
    SECRET_KEY = config('SECRET_KEY')
    SECURITY_PASSWORD_SALT = config('PASSWORD_SALT')
    MAIL_SERVER = str(config('MAIL_DEFAULT_SERVER'))
    MAIL_PORT = int(config('MAIL_PORT'))
    MAIL_USERNAME = str(config('MAIL_USERNAME'))
    MAIL_PASSWORD = str(config('MAIL_PASSWORD'))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(MainConfig):
    SQLALCHEMY_DATABASE_URI = config('PRODUCTION_URI')


class DevelopmentConfig(MainConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config('DEVELOPMENT_URI')

class TestingConfig(MainConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = config('TESTING_URI')
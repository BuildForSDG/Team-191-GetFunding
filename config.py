import random
import os
import string

if os.path.exists("mysecret.txt"):
    f = open('mysecret.txt')
    random_string = f.readline()
else:
    char_set = string.ascii_uppercase + string.digits
    random_string = ''.join(random.sample(char_set*100, 100))
    with open('mysecret.txt', 'a') as the_file:
        the_file.write(random_string)


class Config():
    DEBUG = False
    TESTING = False
    SECRET_KEY = random_string
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DB_NAME = 'ProductionCreditScore'
    SQLALCHEMY_DATABASE_URI = ('''postgresql+psycopg2://cycks:Actuarial2012@
                                    localhost/production''')


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = 'DevelopmentCreditScore'
    SQLALCHEMY_DATABASE_URI = ('''postgresql+psycopg2://cycks:Actuarial2012@
                                    localhost/development''')


class TestingConfig(Config):
    TESTING = True
    DB_NAME = 'TestingCreditScore'
    SQLALCHEMY_DATABASE_URI = ('''postgresql+psycopg2://cycks:Actuarial2012@
                                    localhost/testing''')

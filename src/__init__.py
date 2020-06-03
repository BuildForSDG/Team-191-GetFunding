"""src module."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os
db = SQLAlchemy()
login = LoginManager()
mail = Mail()
from src import models
from decouple import config

def create_app():
    main_app = Flask(__name__)
    main_app.config.from_object(config('SDG_CONFIG'))
    main_app.config['MAIL_SERVER']='smtp.gmail.com'
    main_app.config['MAIL_PORT'] = 465
    main_app.config['MAIL_USERNAME'] = 'mwadimemakokha@gmail.com'
    main_app.config['MAIL_PASSWORD'] = 'SaminSky1'
    main_app.config['MAIL_USE_TLS'] = False
    main_app.config['MAIL_USE_SSL'] = True
    with main_app.app_context():
        db.init_app(main_app)
        mail.init_app(main_app)
        login.init_app(main_app)
        from src.Users import register_bp
        main_app.register_blueprint(register_bp)
        db.create_all()
    return main_app


def print_modules():
    print(dir(models))

"""src module."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()
from src import models
from decouple import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config('SDG_CONFIG'))
    with app.app_context():
        db.init_app(app)
        from src.Users import register_bp
        app.register_blueprint(register_bp)
        db.create_all()
    return app


def print_modules():
    print(dir(models))

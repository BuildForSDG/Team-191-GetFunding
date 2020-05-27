"""src module."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()
from src import models


def create_app():
    app = Flask(__name__)
    if app.config['ENV'] == "production":
        app.config.from_object("configuration.ProductionConfig")
    elif app.config['ENV'] == "development":
        app.config.from_object("configuration.DevelopmentConfig")
    else:
        app.config.from_object("configuration.TestingConfig")

    with app.app_context():
        db.init_app(app)
        from src.Users import register_bp
        app.register_blueprint(register_bp)
        db.create_all()
    return app


def print_modules():
    print(dir(models))

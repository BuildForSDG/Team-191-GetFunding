""" src module.
Every thing application is here
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['SDG_CONFIG'])
    with app.app_context():
        db.init_app(app)
        from .Users import register_bp
        app.register_blueprint(register_bp)
        db.create_all()
    return app

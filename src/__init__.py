"""src module."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing



app = Flask(__name__)


if app.config['ENV'] == "production":
	app.config.from_object("configuration.ProductionConfig")
elif app.config['ENV'] == "development":
	app.config.from_object("configuration.DevelopmentConfig")
elif app.config['ENV'] == "testing":
	app.config.from_object("configuration.TestingConfig")
else:
	pass


db = SQLAlchemy(app)
hashing = Hashing(app)

# from Senddata.send_endpoints import assign_send_data_routes
# from Users.users import assign_my_users_routes

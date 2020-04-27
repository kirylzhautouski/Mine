from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from app.articlesapi import bp as articlesapi_bp
from app.users import bp as users_bp
app.register_blueprint(articlesapi_bp, url_prefix='/articles-api')
app.register_blueprint(users_bp, url_prefix='/users')

from app import app

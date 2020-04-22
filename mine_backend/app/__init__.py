from flask import Flask
from flask_pymongo import PyMongo

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

from app.articlesapi import bp as articlesapi_bp
app.register_blueprint(articlesapi_bp, url_prefix='/articles-api')

from app import app

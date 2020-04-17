from flask import Flask

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.articlesapi import bp as articlesapi_bp
app.register_blueprint(articlesapi_bp, url_prefix='/articles-api')

from app import app

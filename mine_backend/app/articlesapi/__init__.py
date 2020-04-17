from flask import Blueprint

bp = Blueprint('articlesapi', __name__)

from app.articlesapi import routes

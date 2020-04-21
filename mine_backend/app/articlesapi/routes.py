from flask import jsonify

from app.articlesapi import bp
from app.articlesapi.scrapers import TheFlowScraper


@bp.route('/')
def index():
    # return jsonify(TheFlowScraper.scrap_article('https://the-flow.ru/features/kanye-west-gq'))
    return jsonify(TheFlowScraper.scrap_article('https://the-flow.ru/news/bionicle-action-rpg'))

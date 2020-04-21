from flask import jsonify, request, abort

from app.articlesapi import bp
from app.articlesapi.scrapers import TheFlowScraper


@bp.route('/')
def index():
    return jsonify(TheFlowScraper.scrap_article('https://the-flow.ru/features/kanye-west-gq'))
    # return jsonify(TheFlowScraper.scrap_article('https://the-flow.ru/releases/mike-dean-4-20'))


@bp.route('/summary/')
def summary():
    link = request.args.get('link')
    if link:
        return jsonify(TheFlowScraper.get_article_summary(link))
    else:
        abort(400, 'You should provide link query parameter')

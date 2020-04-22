import json

from flask import jsonify, request, abort, Response

from app import app
from app.articlesapi import bp
from app.articlesapi.scrapers import TheFlowScraper
from app.articlesapi.scrapers.article import ArticleJSONEncoder


@bp.route('/')
def index():
    return Response(json.dumps(TheFlowScraper.scrap_article('https://the-flow.ru/features/kanye-west-gq'),
                               cls=ArticleJSONEncoder), mimetype=app.config["JSONIFY_MIMETYPE"])


@bp.route('/summary/')
def summary():
    link = request.args.get('link')
    if link:
        return jsonify(TheFlowScraper.get_article_summary(link))
    else:
        abort(400, 'You should provide link query parameter')


@bp.route('/article/<id>', methods=['POST'])
def save_article(id):
    return jsonify({
        'id': id,
        'method': 'POST',
    })


@bp.route('/article/<id>', methods=['GET'])
def get_article(id):
    return jsonify({
        'id': id,
        'method': 'GET',
    })

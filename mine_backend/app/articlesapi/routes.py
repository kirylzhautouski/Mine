from bson.errors import InvalidId
from flask import jsonify, request, abort, Response
from flask_pymongo import ObjectId

from app import app, mongo
from app.articlesapi import bp
from app.articlesapi.scrapers import TheFlowScraper


@bp.route('/')
def index():
    return jsonify(TheFlowScraper.scrap_article('https://the-flow.ru/features/kanye-west-gq').to_dict())


@bp.route('/summary/')
def summary():
    link = request.args.get('link')
    if link:
        return jsonify(TheFlowScraper.get_article_summary(link))
    else:
        abort(400, 'You should provide link query parameter')


@bp.route('/articles/', methods=['POST'])
def save_article():
    link = request.json.get('link')
    if link:
        result = mongo.db.saved_articles.insert_one(TheFlowScraper
                                                    .scrap_article(link)
                                                    .to_dict())
        return jsonify({
            'insertedId': str(result.inserted_id),
        }), 201
    else:
        return abort(400, 'You should provide a link parameter in body.')


@bp.route('/articles/', methods=['GET'])
def get_articles():
    articles = list(mongo.db.saved_articles.find())

    for article in articles:
        article['_id'] = str(article['_id'])

    return jsonify({
        'articles': articles,
    })


@bp.route('/articles/<id>/', methods=['GET'])
def get_article(id):
    article = mongo.db.saved_articles.find_one_or_404(ObjectId(id))
    article['_id'] = str(article['_id'])

    return jsonify(article)


@bp.route('/articles/<id>/', methods=['DELETE'])
def delete_article(id):
    try:
        mongo.db.saved_articles.delete_one({'_id': ObjectId(id)})
        return Response(status=204)
    except InvalidId as ex:
        return jsonify({
            'errorMessage': str(ex),
        }), 400

from bson.errors import InvalidId
from flask import jsonify, request, abort, Response
from flask_pymongo import ObjectId
from flask_jwt_extended import jwt_required, current_user

from app import app, mongo
from app.articlesapi import bp
from app.articlesapi.scrapers import TheFlowScraper, UnknownChildType, UnknownTagName
from app.request_params import get_int_arg


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
@jwt_required
def save_article():
    link = request.json.get('link')
    if link:
        try:
            article_dict = TheFlowScraper.scrap_article(link).to_dict()
        except (UnknownTagName, UnknownChildType) as ex:
            return abort(500, str(ex))

        article_dict['user_id'] = current_user.object_id

        result = mongo.db.saved_articles.insert_one(article_dict)
        return jsonify({
            'insertedId': str(result.inserted_id),
        }), 201
    else:
        return abort(400, 'You should provide a link parameter in body.')


@bp.route('/articles/', methods=['GET'])
@jwt_required
def get_articles():
    limit = get_int_arg(request, 'limit', 20)
    offset = get_int_arg(request, 'offset', 0)

    articles = list(mongo.db.saved_articles.find({'user_id': current_user.object_id}, skip=offset, limit=limit))

    for article in articles:
        article['_id'] = str(article['_id'])
        article['user_id'] = str(article['user_id'])

    return jsonify({
        'articles': articles,
    })


@bp.route('/articles/<id>/', methods=['GET'])
@jwt_required
def get_article(id):
    article = mongo.db.saved_articles.find_one_or_404({'_id': ObjectId(id), 'user_id': current_user.object_id})
    article['_id'] = str(article['_id'])
    article['user_id'] = str(article['user_id'])

    return jsonify(article)


@bp.route('/articles/<id>/', methods=['DELETE'])
@jwt_required
def delete_article(id):
    try:
        mongo.db.saved_articles.delete_one({'_id': ObjectId(id), 'user_id': current_user.object_id})
        return Response(status=204)
    except InvalidId as ex:
        return jsonify({
            'errorMessage': str(ex),
        }), 400

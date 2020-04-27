from flask import request, jsonify, abort
from flask_jwt_extended import create_access_token, create_refresh_token

from app.users import bp
from app.users.models import User, ValidationError


@bp.route('/register/', methods=['POST'])
def index():
    email = request.json.get('email')
    login = request.json.get('login')
    password = request.json.get('password')

    try:
        new_user = User(email, login, password)
        new_user.save()

        access_token = create_access_token(identity=new_user.id, fresh=True)
        refresh_token = create_refresh_token(new_user.id)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
        }), 201
    except ValidationError as ex:
        return abort(400, str(ex))

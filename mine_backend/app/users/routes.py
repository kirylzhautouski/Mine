from flask import request, jsonify, abort
from flask_jwt_extended import (
    jwt_refresh_token_required, get_jwt_identity, create_access_token,
    jwt_required, current_user
)

from app.request_params import get_str_param
from app.users import bp
from app.users.models import User, ValidationError


@bp.route('/', methods=['GET'])
@jwt_required
def index():
    return jsonify({
        'current_user': current_user.__dict__,
    }), 200


@bp.route('/register/', methods=['POST'])
def register():
    email = get_str_param(request, 'email')
    login = get_str_param(request, 'login')
    password = get_str_param(request, 'password')

    try:
        new_user = User(email, login)
        new_user.set_password(password)
        new_user.save()

        return jsonify(new_user.generate_tokens()), 201
    except ValidationError as ex:
        return abort(400, str(ex))


@bp.route('/login/', methods=['POST'])
def login():
    login = get_str_param(request, 'login')
    password = get_str_param(request, 'password')

    user = User.get_user_by_login(login)
    if user and user.check_password(password):
        return jsonify(user.generate_tokens()), 200

    return abort(401, 'Invalid credentials!')


@bp.route('/refresh-token/', methods=['POST'])
@jwt_refresh_token_required
def refresh_access_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id, fresh=False)
    return jsonify({
        'access_token': access_token
    }), 200

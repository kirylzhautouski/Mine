from flask import request, jsonify, abort

from app.request_params import get_str_param
from app.users import bp
from app.users.models import User, ValidationError


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

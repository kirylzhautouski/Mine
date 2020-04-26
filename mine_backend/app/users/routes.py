from flask import request, jsonify

from app.users import bp


@bp.route('/')
def index():
    email = request.json.get('email')
    login = request.json.get('login')
    password = request.json.get('password')

    return jsonify({
        'email': email,
        'login': login,
        'password': password,
    })

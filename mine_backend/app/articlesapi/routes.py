from app.articlesapi import bp


@bp.route('/')
def index():
    return 'Hello from Flask!'

from flask import Blueprint


bp = Blueprint('noticias', __name__, url_prefix='/noticias')


@bp.route('/')
def root():
    return 'Hello from noticias'


def init_app(app):
    app.register_blueprint(bp)
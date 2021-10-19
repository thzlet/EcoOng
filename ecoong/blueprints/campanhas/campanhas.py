from flask import Blueprint


bp = Blueprint('campanhas', __name__, url_prefix='/campanhas')


@bp.route('/')
def root():
    return 'Hello from campanhas'


def init_app(app):
    app.register_blueprint(bp)
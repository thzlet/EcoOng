from flask import Flask
from ecoong.ext import configuration
from .views import root, buscar_info

def create_app():
    app = Flask(__name__)
    configuration.init_app(app)

    app.add_url_rule('/', view_func=root)
    app.add_url_rule('/busca', view_func=buscar_info, methods=["POST"])

    return app

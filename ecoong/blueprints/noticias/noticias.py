from flask import Blueprint, render_template

from ..noticias.entidades import Noticia


bp = Blueprint('noticias', __name__, static_folder='static_not', template_folder='templates_not', url_prefix='/noticias')


noticia = [
    {'id_noticia': 1, 'titulo': 'Lorem Ipsum', 'imagem': 'static_not/noticias/img/noticia_onze.jpg', 'autor': 'Jubileu', 'data': '19/10/2021', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sollicitudin suscipit elit.', 'categoria': 'Lorem', 'tag': '#Ipsum',},
    {'id_noticia': 2, 'titulo': 'Lorem Ipsum', 'imagem': 'static_not/noticias/img/noticia_doze.jpg', 'autor': 'Jubileu', 'data': '19/10/2021', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sollicitudin suscipit elit.', 'categoria': 'Lorem', 'tag': '#Ipsum',},
    {'id_noticia': 3, 'titulo': 'Lorem Ipsum', 'imagem': 'static_not/noticias/img/noticia_treze.jpg', 'autor': 'Jubileu', 'data': '19/10/2021', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sollicitudin suscipit elit.', 'categoria': 'Lorem', 'tag': '#Ipsum',},
]

@bp.route('/noticias')
def noticias_page():
    return render_template('noticias/noticia.html', noticias=noticia)

@bp.route('/detalhe_not')
def detalhe_not_page():
    return render_template('noticias/detalhe_noticia.html')

def init_app(app):
    app.register_blueprint(bp)
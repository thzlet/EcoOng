from flask import Blueprint, render_template, request, redirect, flash, url_for

from ..noticias.entidades import Noticia

from ecoong.ext.database import db

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


@bp.route('/cad_noticia', methods=['GET', 'POST'])
def cadastro_not():
    if request.method == 'POST':
        noticia = Noticia()
        noticia.titulo = request.form['titulo']
        noticia.autor = request.form['autor']
        noticia.data  = request.form['data']
        noticia.descricao = request.form['des']

        db.session.add(noticia)
        db.session.commit()

        flash('Notícia publicada')

        return redirect(url_for('noticias.noticias_page'))

    return render_template('noticias/post_not.html')


def init_app(app):
    app.register_blueprint(bp)

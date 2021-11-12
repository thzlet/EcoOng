import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
from ..noticias.entidades import Noticia
from ecoong.models import Membro
from flask_login import current_user
from ecoong.ext.database import db
from ... import create_app


bp = Blueprint('noticias', __name__, static_folder='static_not', template_folder='templates_not', url_prefix='/noticias')


noticia = [
    {'id_noticia': 1, 'titulo': 'Lorem Ipsum', 'imagem': 'static_not/noticias/img/noticia_onze.jpg', 'autor': 'Jubileu', 'data': '19/10/2021', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sollicitudin suscipit elit.', 'categoria': 'Lorem', 'tag': '#Ipsum',},
    {'id_noticia': 2, 'titulo': 'Lorem Ipsum', 'imagem': 'static_not/noticias/img/noticia_doze.jpg', 'autor': 'Jubileu', 'data': '19/10/2021', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sollicitudin suscipit elit.', 'categoria': 'Lorem', 'tag': '#Ipsum',},
    {'id_noticia': 3, 'titulo': 'Lorem Ipsum', 'imagem': 'static_not/noticias/img/noticia_treze.jpg', 'autor': 'Jubileu', 'data': '19/10/2021', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sollicitudin suscipit elit.', 'categoria': 'Lorem', 'tag': '#Ipsum',},
]


FORMATOS_PERMITIDOS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FORMATOS_PERMITIDOS


@bp.route('/noticias')
def noticias_page():
    notc = Noticia.query.all()
    return render_template('noticias/noticia.html', noticias=noticia, noticiass = notc)


@bp.route('/detalhe_not')
def detalhe_not_page():
    return render_template('noticias/detalhe_noticia.html')


@bp.route('/cad_noticia', methods=['GET', 'POST'])
def cadastrar_not():
    if request.method == 'POST':
        noticia = Noticia()
        noticia.titulo = request.form['titulo']
        noticia.autor = request.form['autor']
        noticia.data  = request.form['data']
        noticia.descricao = request.form['des']
        foto = request.files['img']
        noticia.membro_id = Membro.query.get(current_user.id)

        if foto and allowed_file(foto.filename):
            noticia.img_not = foto.filename

            app = create_app()
            foto.save(os.path.join(app.config['UPLOAD_NOTICIA'], foto.filename))


            current_user.noticia.append(noticia)
            db.session.commit()

            flash('Notícia publicada')

        else:
            flash("Apenas extensões 'png', 'jpg', 'jpeg'!")
            return redirect('/noticias/cadastrar_noticia.html')

        return redirect(url_for('noticias.noticias_page'))

    return render_template('noticias/cadastrar_noticia.html')


@bp.get('/imagem/<nome>')
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_NOTICIA'], nome)


def init_app(app):
    app.register_blueprint(bp)

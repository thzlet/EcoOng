import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
from ..noticias.entidades import Noticia
from ecoong.models import Membro
from flask_login import current_user
from ecoong.ext.database import db
from ... import create_app
from werkzeug.utils import secure_filename
import datetime


bp = Blueprint('noticias', __name__, static_folder='static_not', template_folder='templates_not', url_prefix='/noticias')

FORMATOS_PERMITIDOS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FORMATOS_PERMITIDOS


@bp.route('/noticias')
def noticias_page():
    notc = Noticia.query.all()
    return render_template('noticias/noticia.html', noticias = notc)


@bp.route('/detalhe_not/<id>')
def detalhe_not_page(id):
    notc = Noticia.query.get(id)
    return render_template('noticias/detalhe_noticia.html', noticia = notc)


@bp.route('/cad_noticia', methods=['GET', 'POST'])
def cadastrar_not():
    if request.method == 'POST':
        noticia = Noticia()
        noticia.titulo = request.form['titulo']
        noticia.autor = request.form['nome']
        noticia.descricao = request.form['des']
        foto = request.files['img']

        data = request.form['data']
        hora = request.form['hora']
        datahora = datetime.datetime.fromisoformat(f'{data} {hora}')
        noticia.datahora = datahora
        #noticia.datahora = datetime.datetime.fromisoformat(f'{data} {hora}')

        noticia.membro_id = Membro.query.get(current_user.id)

        current_user.noticia.append(noticia)
        db.session.commit()

        if foto and allowed_file(foto.filename):
            filename =  secure_filename(foto.filename)
            filename = filename.split('.')
            filename = f'noticia_{noticia.id}.{filename[1]}'
            noticia.img_not = filename

            app = create_app()
            foto.save(os.path.join(app.config['UPLOAD_NOTICIA'], filename))

            current_user.noticia.append(noticia)
            db.session.commit()

            flash('Notícia publicada')

        else:
            flash("Apenas extensões 'png', 'jpg', 'jpeg'!")
            return redirect(url_for('noticias.cadastrar_not'))


    now = str(datetime.datetime.utcnow()).split(' ')[0]
    return render_template('noticias/cadastrar_noticia.html', now=now)


@bp.get('/imagem/<nome>')
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_NOTICIA'], nome)


def init_app(app):
    app.register_blueprint(bp)

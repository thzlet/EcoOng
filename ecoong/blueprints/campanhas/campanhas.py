import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
from ..campanhas.entidades import Campanha
from ecoong.models import Membro
from flask_login import current_user
from ecoong.ext.database import db
from ... import create_app
from werkzeug.utils import secure_filename

bp = Blueprint('campanhas', __name__,static_folder='static_cam', template_folder='templates_cam', url_prefix='/campanhas')


FORMATOS_PERMITIDOS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FORMATOS_PERMITIDOS


campanha = [
    {'id_campanha': 1, 'titulo': 'A AMAZÔNIA É O BRASIL', 'imagem': 'static_cam/campanhas/img/Campanhas_1.jpg', 'descricao': 'O desmatamento destrói ecossistemas e coloca milhões de vidas em risco. Nos ajude a combatê-lo!'},
    {'id_campanha': 2, 'titulo': 'PROTEJA O OCEANO', 'imagem': 'static_cam/campanhas/img/Campanhas_2.jpg', 'descricao': 'Nossos oceanos estão sob ameaça! Temos a chance de mudar esse caminho que parece sem volta.'},
    {'id_campanha': 3, 'titulo': 'SOS MATA ATLÂNTICA', 'imagem': 'static_cam/campanhas/img/Campanhas_3.jpg', 'descricao': 'Precisamos recuperar a floresta, além de fortalecer a legislação que a protege.'},
    {'id_campanha': 4, 'titulo': 'ÁGUA PARA TODOS', 'imagem': 'static_cam/campanhas/img/Campanhas_4.jpg', 'descricao': 'A escassez de água é um problema que afeta 35 milhões de brasileiros. Nos ajude a combatê-la!'},
    {'id_campanha': 5, 'titulo': 'TRÁFICO DE ANIMAIS', 'imagem': 'static_cam/campanhas/img/Campanhas_5.jpg', 'descricao': 'A sua doação nos ajudará a salvar milhares de animais silvestres do comércio ilegal.'},
    {'id_campanha': 6, 'titulo': 'FIM DOS LIXÕES', 'imagem': 'static_cam/campanhas/img/Campanhas_6.jpg', 'descricao': 'Além da poluição, a má gestão dos resíduos tem efeitos prejudiciais à saúde pública.'},
    ]


@bp.route('/campanhas')
def campanha_page():
    camp = Campanha.query.all()
    return render_template('campanhas/campanha.html', campanhas=campanha, campanhass = camp)


@bp.route('/detalhe_cam/<id>')
def detalhe_cam_page(id):
    cam = Campanha.query.get(id)
    return render_template('campanhas/detalhe_campanha.html', campanha=cam)


@bp.route('/doacao')
def doacao_page():
    return render_template('campanhas/doacoes.html')


@bp.route('/cad_campanha', methods=['GET', 'POST'])
def cadastrar_cam():
    if request.method == 'POST':
        campanha = Campanha()
        campanha.titulo = request.form['titulo']
        campanha.descricao = request.form['des']
        foto = request.files['img']
        campanha.membro_id = Membro.query.get(current_user.id)

        current_user.campanha.append(campanha)
        db.session.commit()

        if foto and allowed_file(foto.filename):
            filename =  secure_filename(foto.filename)
            filename = filename.split('.')
            filename = f'campanha_{campanha.id}.{filename[1]}'
            campanha.img_cam = filename

            app = create_app()
            foto.save(os.path.join(app.config['UPLOAD_CAMPANHA'], filename))

            current_user.campanha.append(campanha)
            db.session.commit()

            flash('campanha publicada')

        else:
            flash("Apenas extensões 'png', 'jpg', 'jpeg'!")
            return redirect('/campanhas/cadastrar_campanha.html')

        return redirect(url_for('campanhas.campanha_page'))

    return render_template('campanhas/cadastrar_campanha.html')


@bp.get('/imagem/<nome>')
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_CAMPANHA'], nome)


def init_app(app):
    app.register_blueprint(bp)
import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
from flask_login import login_required
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


@bp.route('/campanhas')
def campanha_page():
    camp = Campanha.query.all()
    return render_template('campanhas/campanha.html', campanhas = camp)


@bp.route('/detalhe_cam/<id>')
def detalhe_cam_page(id):
    cam = Campanha.query.get(id)
    return render_template('campanhas/detalhe_campanha.html', campanha=cam)


@bp.route('/doacao')
def doacao_page():
    return render_template('campanhas/doacoes.html')

@bp.route('/agradecimento')
def agradecimento_page():
    return render_template('campanhas/agradecimento.html')

@bp.route('/dadosdoacaocard')
@login_required
def dadosdoacaocard_page():
    return render_template('campanhas/dadosdoacaocard.html')

@bp.route('/dadosdoacaopix')
@login_required
def dadosdoacaopix_page():
    return render_template('campanhas/dadosdoacaopix.html')


@bp.route('/cad_campanha', methods=['GET', 'POST'])
def cadastrar_cam():
    if request.method == 'POST':
        campanha = Campanha()
        campanha.titulo = request.form['titulo']
        campanha.autor = request.form['autor']
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


#remover campanha
@bp.route('/remover/<id>', methods=['GET', 'POST'])
@login_required
def remover_cam(id):
    campanha = Campanha.query.get(id)
    if campanha.img_cam == 'img_cam_padrao.png':
        db.session.delete(campanha)
        db.session.commit()

        flash('Campanha apagada!')

        return redirect(url_for('membros.historico'))

    else:
        app = create_app()
        os.remove(os.path.join(app.config['UPLOAD_CAMPANHA'], campanha.img_cam))

        db.session.delete(campanha)
        db.session.commit()

        flash('Campanha apagada!')

        return redirect(url_for('membros.historico'))


#editar campanha
@bp.route('/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar_cam(id):
    campanha = Campanha.query.get(id)
    if request.method == 'POST':
        campanha.titulo = request.form['titulo']
        campanha.autor = request.form['autor']
        descricao = request.form['des']
        campanha.membro_id = current_user.id
        if descricao != '':
            campanha.descricao = descricao
        db.session.commit()

        if 'img' in request.files:
            foto = request.files['img']

            if foto:
                if allowed_file(foto.filename):
                    filename =  secure_filename(foto.filename)
                    filename = filename.split('.')
                    filename = f'campanha_{campanha.id}.{filename[1]}'
                    campanha.img_cam = filename

                    app = create_app()
                    foto.save(os.path.join(app.config['UPLOAD_CAMPANHA'], filename))

                    current_user.campanha.append(campanha)
                    db.session.commit()

                    flash('Campanha atualizada')
                else:
                    flash("Apenas extensões 'png', 'jpg', 'jpeg'!")
                    return redirect(url_for('membros.historico'))
        else:
            current_user.campanha.append(campanha)
            db.session.commit()

            flash('Campanha atualizada')

        return redirect(url_for('membros.historico'))

    return render_template('campanhas/editar_campanha.html', campanha = campanha)


def init_app(app):
    app.register_blueprint(bp)
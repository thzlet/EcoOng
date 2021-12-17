import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
from flask_login import login_required, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField
from wtforms.validators import DataRequired

from ..campanhas.entidades import Campanha
from ecoong.models import Membro

from ecoong.ext.database import db
from ... import create_app

from werkzeug.utils import secure_filename

from sqlalchemy import or_


bp = Blueprint('campanhas', __name__,static_folder='static_cam', template_folder='templates_cam', url_prefix='/campanhas')


#FORMULARIOS
class CadastroCampanhaForm(FlaskForm):
    autor = StringField(name='autor', render_kw={'readonly':True})
    titulo = StringField(name='titulo', validators=[DataRequired()])
    descricao = TextAreaField(name='descricao',render_kw={'cols':'50', 'rols':'5'}, validators=[DataRequired()])
    imagem = FileField(name='img', validators=[DataRequired()])


class EditarCampanhaForm(FlaskForm):
    autor = StringField(name='autor', render_kw={'readonly':True})
    titulo = StringField(name='titulo')
    descricao = TextAreaField(name='descricao', render_kw={'cols':'50', 'rols':'5'})
    imagem = FileField(name='img')


class DadosCartaoForm(FlaskForm):
    nome = StringField(name='nome', validators=[DataRequired()])
    cpf = StringField(name='cpf', validators=[DataRequired()])
    bandeira = StringField(name='bandeira', validators=[DataRequired()])
    numero = StringField(name='numero', validators=[DataRequired()])
    banco = StringField(name='banco', validators=[DataRequired()])
    vencimento = StringField(name='vencimento', validators=[DataRequired()])


class BuscarCampanhaForm(FlaskForm):
    busca = StringField(name='busca', validators=[DataRequired()])


#FORMATO DE IMAGEM PERMITIDA
FORMATOS_PERMITIDOS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FORMATOS_PERMITIDOS


#PAGINA DE CAMPANHAS
@bp.route('/campanhas')
def campanha_page():
    form = BuscarCampanhaForm()
    camp = Campanha.query.order_by(Campanha.id.desc()).all()
    return render_template('campanhas/campanha.html', campanhas = camp, form = form)


#DETALHE DE CAMPANHAS
@bp.route('/detalhe_cam/<id>')
def detalhe_cam_page(id):
    cam = Campanha.query.get(id)
    return render_template('campanhas/detalhe_campanha.html', campanha=cam)


#PAGINA DE DOAÇOES
@bp.route('/doacao')
def doacao_page():
    return render_template('campanhas/doacoes.html')


#PAGINA DE AGRADECIMENTOS
@bp.route('/agradecimento')
@login_required
def agradecimento_page():
    return render_template('campanhas/agradecimento.html')


#FORMULARIO DE DOAÇAO POR CARTAO
@bp.route('/dadosdoacaocard')
@login_required
def dadosdoacaocard_page():
    form = DadosCartaoForm()
    return render_template('campanhas/dadosdoacaocard.html', form = form)


#DOAÇAO POR PIX
@bp.route('/dadosdoacaopix')
@login_required
def dadosdoacaopix_page():
    return render_template('campanhas/dadosdoacaopix.html')


#CADASTRAR DE CAMPANHA
@bp.route('/cad_campanha', methods=['GET', 'POST'])
@login_required
def cadastrar_cam():
    form = CadastroCampanhaForm()
    if request.method == 'POST':
        campanha = Campanha()
        campanha.titulo = form.titulo.data
        campanha.autor = form.autor.data
        campanha.descricao = form.descricao.data
        foto = form.imagem.data
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

            flash('Campanha publicada!')

        else:
            flash("Apenas extensões 'png', 'jpg', 'jpeg'!")
            return redirect(url_for('campanhas.cadastrar_cam'))

        return redirect(url_for('campanhas.campanha_page'))

    form.autor.data = current_user.nome
    return render_template('campanhas/cadastrar_campanha.html', form = form)

#EXIBIR IMAGEM DA CAMPANHA
@bp.get('/imagem/<nome>')
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_CAMPANHA'], nome)


#REMOVER CAMPANHA
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


#EDITAR CAMPANHA
@bp.route('/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar_cam(id):
    form = EditarCampanhaForm()
    campanha = Campanha.query.get(id)
    if request.method == 'POST':
        campanha.titulo = form.titulo.data
        campanha.autor = form.autor.data
        descricao = form.descricao.data
        campanha.membro_id = current_user.id
        if descricao != '':
            campanha.descricao = descricao
        db.session.commit()

        if 'img' in request.files:
            foto = form.imagem.data

            if foto:
                if allowed_file(foto.filename):
                    filename =  secure_filename(foto.filename)
                    filename = filename.split('.')
                    filename = f'campanha_{campanha.id}.{filename[1]}'
                    campanha.img_cam = filename

                    app = create_app()
                    foto.save(os.path.join(app.config['UPLOAD_CAMPANHA'], filename))

                else:
                    flash("Apenas extensões 'png', 'jpg', 'jpeg'!")
                    return redirect(url_for('membros.historico'))

        current_user.campanha.append(campanha)
        db.session.commit()

        flash('Campanha atualizada!')

        return redirect(url_for('membros.historico'))

    form.titulo.data = campanha.titulo
    form.autor.data = current_user.nome
    form.descricao.data = campanha.descricao
    return render_template('campanhas/editar_campanha.html', campanha = campanha, form = form)


#BUSCAR CAMPANHA
@bp.post('/busca')
def buscar_cam():
    form = BuscarCampanhaForm()
    busca = form.busca.data
    search = '%{}%'.format(busca)
    cam = Campanha.query.filter(or_(Campanha.titulo.like(search), Campanha.descricao.like(search))).all()

    return render_template('campanhas/exibir_campanhas_buscada.html', campanhas = cam, form = form)


def init_app(app):
    app.register_blueprint(bp)

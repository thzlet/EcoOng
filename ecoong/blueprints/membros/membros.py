import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user

from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, FileField, BooleanField, IntegerField

from ecoong.blueprints.campanhas.entidades import Campanha
from ecoong.blueprints.noticias.entidades import Noticia
from ecoong.models import Membro
from ecoong.ext.database import db

from ... import create_app

from werkzeug.utils import secure_filename


bp = Blueprint('membros', __name__,static_folder='static_mem', template_folder='templates_mem', url_prefix='/membros')


#FORMULARIO
class AtualizarDadosForm(FlaskForm):
    nome = StringField(name='nv_nome', id='nome')
    fotoperfil = FileField(name='nv_img', id='fotoperfil')
    removerfoto = BooleanField(name="remover_foto", id="flexCheckDefault")
    email = EmailField(name='nv_email', id='email')
    telefone = StringField(name='nv_tel', id='tel')
    idade = IntegerField(name='nv_idade', id='idade')


##FORMATO DE IMAGEM PERMITIDA
FORMATOS_PERMITIDOS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FORMATOS_PERMITIDOS


#VISUALIZAR PERFIL
@bp.route('/perfil')
@login_required
def perfil_page():
    return render_template('membros/perfil.html')


#ATUALIZAR DADOS
@bp.route('/atualizar', methods=['GET', 'POST'])
def atualizar_page():
    form = AtualizarDadosForm()
    if request.method == 'POST':
        alguem_com_o_email_desejado = Membro.query.filter_by(email=request.form['nv_email']).first()
        if alguem_com_o_email_desejado is not None and alguem_com_o_email_desejado.id != current_user.id:
            flash('Esse email ja existe')
        else:
            membro = Membro.query.get(current_user.id)
            membro.nome = form.nome.data
            membro.email = form.email.data
            membro.telefone = form.telefone.data
            membro.idade = int(form.idade.data)
            foto = form.fotoperfil.data
            remover_foto = form.removerfoto.data

            if foto and allowed_file(foto.filename):
                if current_user.img_perfil != 'img_padrao.jpg':
                    app = create_app()
                    os.remove(os.path.join(app.config['UPLOAD_PERFIL'], membro.img_perfil))

                filename =  secure_filename(foto.filename)
                filename = filename.split('.')
                filename = f'perfil_{membro.id}.{filename[1]}'
                membro.img_perfil = filename

                app = create_app()
                foto.save(os.path.join(app.config['UPLOAD_PERFIL'], filename))
            else:
                flash("Apenas extensões 'png', 'jpg', 'jpeg'!")
                return redirect(url_for('membros.atualizar_page'))

            if remover_foto == True:
                if current_user.img_perfil != 'img_padrao.jpg':
                    app = create_app()
                    os.remove(os.path.join(app.config['UPLOAD_PERFIL'], membro.img_perfil))

                    current_user.img_perfil = 'img_padrao.jpg'

            db.session.add(membro)
            db.session.commit()

            flash('Atualização concluído!')

            return redirect(url_for('membros.perfil_page'))

    form.nome.data = current_user.nome
    form.email.data = current_user.email
    form.telefone.data = current_user.telefone
    form.idade.data = current_user.idade
    form.fotoperfil.data = current_user.img_perfil
    form.removerfoto.data = False
    return render_template('membros/atualizar_dados.html', form = form)


#EXIBIR FOTO DE PERFIL
@bp.get('/imagem/<nome>')
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_PERFIL'], nome)


#REMOVER MEMBRO
@bp.get('/remover')
def remover_page():
    #removendo membro
    membro = Membro.query.get(current_user.id)

    app = create_app()
    os.remove(os.path.join(app.config['UPLOAD_PERFIL'], membro.img_perfil))

    db.session.delete(membro)
    db.session.commit()

    flash('Sua conta foi apagada')

    return redirect('/')


#HISTORICO
@bp.route('/historico')
def historico():
    notc = Noticia.query.order_by(Noticia.id.desc()).all()
    camp = Campanha.query.order_by(Campanha.id.desc()).all()
    return render_template('membros/historico.html', noticias = notc, campanhas = camp)


def init_app(app):
    app.register_blueprint(bp)

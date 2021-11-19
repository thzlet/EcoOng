import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from ecoong.models import Membro
from ecoong.ext.database import db
from ... import create_app
from werkzeug.utils import secure_filename


bp = Blueprint('membros', __name__,static_folder='static_mem', template_folder='templates_mem', url_prefix='/membros')


FORMATOS_PERMITIDOS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FORMATOS_PERMITIDOS


#visualizar perfil
@bp.route('/perfil')
@login_required
def perfil_page():
    return render_template('membros/perfil.html')


#atualizar dados
@bp.route('/atualizar', methods=['GET', 'POST'])
def atualizar_page():
    if request.method == 'POST':
        alguem_com_o_email_desejado = Membro.query.filter_by(email=request.form['nv_email']).first()
        if alguem_com_o_email_desejado is not None and alguem_com_o_email_desejado.id != current_user.id:
            flash('Esse email ja existe :(')
        else:
            membro = Membro.query.get(current_user.id)
            membro.nome = request.form['nv_nome']
            membro.email = request.form['nv_email']
            membro.telefone = request.form['nv_tel']
            membro.idade = int(request.form['nv_idade'])
            foto = request.files['nv_img']

            if foto and allowed_file(foto.filename):
                filename =  secure_filename(foto.filename)
                filename = filename.split('.')
                filename = f'perfil_{membro.id}.{filename[1]}'
                membro.img_perfil = filename

                app = create_app()
                foto.save(os.path.join(app.config['UPLOAD_PERFIL'], filename))

                db.session.add(membro)
                db.session.commit()

                flash('Atualização concluído :)')

            else:
                db.session.add(membro)
                db.session.commit()

            return redirect(url_for('membros.perfil_page'))

    return render_template('membros/atualizar_dados.html')

@bp.get('/imagem/<nome>')
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_PERFIL'], nome)

#remover membro
@bp.get('/remover')
def remover_page():
    membro = Membro.query.get(current_user.id)

    db.session.delete(membro)
    db.session.commit()

    flash('Sua conta foi apagada')

    return redirect('/')

#buscar informação


#registrando o blueprint membros
def init_app(app):
    app.register_blueprint(bp)

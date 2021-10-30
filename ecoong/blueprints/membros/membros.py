from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ecoong.models import Membro
from ecoong.ext.database import db


bp = Blueprint('membros', __name__,static_folder='static_mem', template_folder='templates_mem', url_prefix='/membros')


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


            db.session.add(membro)
            db.session.commit()

            flash('Atualização concluído :)')

            return redirect(url_for('membros.perfil_page'))

    return render_template('membros/atualizar_dados.html')

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

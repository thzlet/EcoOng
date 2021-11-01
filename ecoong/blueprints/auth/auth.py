from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user

from ecoong.models import Membro
from ecoong.ext.database import db
from ecoong.ext.login import login
from ecoong.ext.bcrypt import bcrypt


bp = Blueprint('auth', __name__,static_folder='static_auth', template_folder='templates_auth', url_prefix='/auth')


@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro_page():
    if request.method == 'POST':
        if Membro.query.filter_by(email=request.form['email']).first() is not None:
            flash('Esse email ja existe :(')
            return redirect(url_for('auth.cadastro_page'))

        membro = Membro()
        membro.nome = request.form['nome']
        membro.email = request.form['email']
        membro.senha  = bcrypt.generate_password_hash(request.form['senha'])
        membro.telefone = request.form['tel']
        membro.idade = int(request.form['idade'])

        db.session.add(membro)
        db.session.commit()

        flash('Cadastro concluído :)')

        return redirect(url_for('auth.login_page'))

    return render_template('auth/cadastro.html')


@bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        verif_email = request.form['email']
        verif_senha = request.form['senha']

        membro = Membro.query.filter_by(email=verif_email).first()
        if membro:
            if bcrypt.check_password_hash(membro.senha,verif_senha):
                login_user(membro)
                flash('Já pode aproveitar as nossas ferramentas ;)')
                return redirect(url_for('membros.perfil_page'))
            else:
                flash('Errou a senha :(')
                return redirect(url_for('auth.login_page'))
        else:
            flash('Usuário nao existe :(')
            return redirect(url_for('auth.login_page'))

    return render_template('auth/login.html')


@bp.get('/logout')
@login_required
def sair():
    logout_user()
    flash('Você saiu! :(')
    return redirect('/')


login.login_view = '/auth/login'
login.login_message = "Faça login para acessar essa página!"


def init_app(app):
    app.register_blueprint(bp)

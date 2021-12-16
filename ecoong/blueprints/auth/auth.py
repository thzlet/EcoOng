from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

from ecoong.models import Membro

from ecoong.ext.database import db
from ecoong.ext.login import login
from ecoong.ext.bcrypt import bcrypt


bp = Blueprint('auth', __name__,static_folder='static_auth', template_folder='templates_auth', url_prefix='/auth')


#FORMULARIOS
class CadastroForm(FlaskForm):
    nome = StringField(name='nome', id='nome', validators=[DataRequired()])
    email = EmailField(name='email', id='email', validators=[DataRequired(message="Tente com @gmail.com"), Email()])
    telefone = StringField(name='tel', id='tel', validators=[DataRequired()])
    idade = IntegerField(name='idade', id='idade', validators=[DataRequired()])
    senha = PasswordField(name='senha', id='senha', validators=[DataRequired(),EqualTo('confirmar', message="A senha deve ser igual")])
    confirmar = PasswordField('')


class LoginForm(FlaskForm):
    email = EmailField(name='email', id='email', validators=[DataRequired(message="Tente com @gmail.com"), Email()])
    senha = PasswordField(name='senha', id='senha', validators=[DataRequired()])


#CADASTRO
@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro_page():
    form = CadastroForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if Membro.query.filter_by(email=form.email.data).first() is not None:
                flash('Esse email já existe!')
                return redirect(url_for('auth.cadastro_page'))

            membro = Membro()
            membro.nome = form.nome.data
            membro.email = form.email.data
            membro.senha  = bcrypt.generate_password_hash(form.senha.data)
            membro.telefone = form.telefone.data
            membro.idade = int(form.idade.data)
            membro.img_perfil = 'img_padrao.jpg'

            db.session.add(membro)
            db.session.commit()

            flash('Cadastro concluído!')

            return redirect(url_for('auth.login_page'))

    return render_template('auth/cadastro.html', form = form)


#LOGIN
@bp.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        verif_email = form.email.data
        verif_senha = form.senha.data

        membro = Membro.query.filter_by(email=verif_email).first()
        if membro:
            if bcrypt.check_password_hash(membro.senha,verif_senha):
                login_user(membro)
                flash('Bem-vindo(a)!')
                return redirect(url_for('membros.perfil_page'))
            else:
                flash('Senha Incorreta!')
                return redirect(url_for('auth.login_page'))
        else:
            flash('Usuário não existe!')
            return redirect(url_for('auth.login_page'))

    return render_template('auth/login.html', form = form)


#LOGOUT
@bp.get('/logout')
@login_required
def sair():
    logout_user()
    flash('Você saiu!')
    return redirect('/')


login.login_view = '/auth/login'
login.login_message = "Faça login para acessar a página!"


def init_app(app):
    app.register_blueprint(bp)

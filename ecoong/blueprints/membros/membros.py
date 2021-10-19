from flask import Blueprint, render_template, request, redirect
from ecoong.models import Membro
from ecoong.ext.database import db

bp = Blueprint('membros', __name__,static_folder='static_mem', template_folder='templates_mem', url_prefix='/membros')


@bp.route('/')
def root():
    return 'Hello from membros'

#rota de cadastro
@bp.route('/cadastro')
def cadastro_page():
    return render_template('membros/cadastro.html')

#salvando os dados digitados no banco de dados
@bp.post('/novocadastro')
def cadastrar_page():
    membro = Membro()
    membro.nome = request.form['nome']
    membro.email = request.form['email']
    membro.senha  = request.form['senha']
    membro.telefone = request.form['tel']
    membro.idade = int(request.form['idade'])

    db.session.add(membro)
    db.session.commit()

    return redirect('/')

#rota de login
@bp.route('/login')
def login_page():
    return render_template('membros/login.html')

#validação de login
@bp.post('/entrar')
def form_login():
    verif_email = request.form['email']
    verif_senha = request.form['senha']

    membro = Membro.query.filter_by(email=verif_email).first()

    if membro:
        if verif_email == membro.email and verif_senha == membro.senha:
            return 'parabensss'
        else:
            return 'algo deu errado'

#atualizar dados

#remover membro

#registrando o blueprint membros
def init_app(app):
    app.register_blueprint(bp)

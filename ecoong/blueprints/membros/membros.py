from flask import Blueprint, render_template


bp = Blueprint('membros', __name__, template_folder='templates_mem', url_prefix='/membros')


@bp.route('/')
def root():
    return 'Hello from membros'

@bp.route('/cadastro')
def cadastro_page():
    #return 'Hello from cadastro'
    return render_template('membros/cadastro.html')

@bp.route('/login')
def login_page():
    return render_template('membros/login.html')

def init_app(app):
    app.register_blueprint(bp)
from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('membros', __name__,static_folder='static_mem', template_folder='templates_mem', url_prefix='/membros')


#visualizar perfil
@bp.route('/perfil')
@login_required
def perfil_page():
    return render_template('membros/perfil.html')


#atualizar dados


#remover membro


#buscar informação


#registrando o blueprint membros
def init_app(app):
    app.register_blueprint(bp)

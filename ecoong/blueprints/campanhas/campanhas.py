from flask import Blueprint, render_template


bp = Blueprint('campanhas', __name__,static_folder='static_cam', template_folder='templates_cam', url_prefix='/campanhas')


campanha = [
    {'id_campanha': 1, 'titulo': 'A AMAZÔNIA É O BRASIL', 'imagem': 'static_cam/campanhas/img/Campanhas_1.jpg', 'descricao': 'O desmatamento destrói ecossistemas e coloca milhões de vidas em risco. Nos ajude a combatê-lo!'},
    {'id_campanha': 2, 'titulo': 'PROTEJA O OCEANO', 'imagem': 'static_cam/campanhas/img/Campanhas_2.jpg', 'descricao': 'Nossos oceanos estão sob ameaça! Temos a chance de mudar esse caminho que parece sem volta.'},
    {'id_campanha': 3, 'titulo': 'SOS MATA ATLÂNTICA', 'imagem': 'static_cam/campanhas/img/Campanhas_3.jpg', 'descricao': 'Precisamos recuperar a floresta, além de fortalecer a legislação que a protege.'},
    {'id_campanha': 4, 'titulo': 'ÁGUA PARA TODOS', 'imagem': 'static_cam/campanhas/img/Campanhas_4.jpg', 'descricao': 'A escassez de água é um problema que afeta 35 milhões de brasileiros. Nos ajude a combatê-la!'},
    {'id_campanha': 5, 'titulo': 'TRÁFICO DE ANIMAIS', 'imagem': 'static_cam/campanhas/img/Campanhas_5.jpg', 'descricao': 'A sua doação nos ajudará a salvar milhares de animais silvestres do comércio ilegal.'},
    {'id_campanha': 6, 'titulo': 'FIM DOS LIXÕES', 'imagem': 'static_cam/campanhas/img/Campanhas_6.jpg', 'descricao': 'Além da poluição, a má gestão dos resíduos tem efeitos prejudiciais à saúde pública.'},
    ]

@bp.route('/campanhas')
def campanha_page():
    return render_template('campanhas/campanha.html',campanhas=campanha)

@bp.route('/detalhe_cam')
def detalhe_cam_page():
    return render_template('campanhas/detalhe_campanha.html')

@bp.route('/doacao')
def doacao_page():
    return render_template('campanhas/doacoes.html')

def init_app(app):
    app.register_blueprint(bp)
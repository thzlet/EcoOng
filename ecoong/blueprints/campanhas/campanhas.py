from flask import Blueprint, render_template


bp = Blueprint('campanhas', __name__,static_folder='static_cam', template_folder='templates_cam', url_prefix='/campanhas')


campanha = [
    {'id_campanha': 1, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_1.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 2, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_2.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 3, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_3.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 4, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_4.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 5, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_5.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 6, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_6.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 7, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_7.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 8, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_8.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 9, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_9.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 10, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_10.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 11, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_11.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
    {'id_campanha': 12, 'titulo': 'Lorem Ipsum', 'imagem': 'static_cam/campanhas/img/Campanhas_12.jpg', 'descricao': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu libero lacus. Morbi consequat egestas lacus.'},
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
from flask import Blueprint, render_template


bp = Blueprint('campanhas', __name__,static_folder='static_cam', template_folder='templates_cam', url_prefix='/campanhas')


campanha = [
    {'id_campanha': 1,
     'titulo': 'Lorem Ipsum',
     'imagem': 'static_cam/campanhas/img/campanha.jpg',
     'descricao': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'
    }
    ]

@bp.route('/campanhas')
def campanha_page():
    return render_template('campanhas/campanha.html',campanhas=campanha)


def init_app(app):
    app.register_blueprint(bp)
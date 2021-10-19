from flask import Blueprint, render_template


bp = Blueprint('noticias', __name__, static_folder='static_not', template_folder='templates_not', url_prefix='/noticias')


noticia = [
    {'id_noticia': 1,
     'titulo': 'Lorem Ipsum',
     'imagem': 'static_not/noticias/img/noticia.jpg',
     'autor': 'Jubileu',
     'data': '19/10/2021',
     'descricao': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
     'categoria': 'Lorem',
     'tag': '#Ipsum',
    }
    ]

@bp.route('/noticias')
def noticias_page():
    return render_template('noticias/noticia.html', noticias=noticia)

def init_app(app):
    app.register_blueprint(bp)
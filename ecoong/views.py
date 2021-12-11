from flask import render_template, request
#from .models import Membro
from ecoong.blueprints.campanhas.entidades import Campanha
from ecoong.blueprints.noticias.entidades import Noticia, Tag
from sqlalchemy import or_

def root():
    camp = Campanha.query.all()
    notc = Noticia.query.all()
    return render_template('index.html', campanhas = camp, noticias = notc)


def buscar_info():
    busca = request.form['busca']
    search = '%{}%'.format(busca)
    notc = Noticia.query.join(Noticia.tags).filter(or_(Noticia.titulo.like(search), Noticia.descricao.like(search), Tag.tag.like(search))).all()
    cam = Campanha.query.filter(Campanha.titulo.like(search)).all()

    return render_template('buscar_informacao.html', noticias = notc, campanhas = cam)

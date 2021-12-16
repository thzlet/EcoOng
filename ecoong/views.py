from flask import render_template

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


from ecoong.blueprints.campanhas.entidades import Campanha
from ecoong.blueprints.noticias.entidades import Noticia, Tag

from sqlalchemy import or_


class BuscarNoticiaForm(FlaskForm):
    busca = StringField(name='busca', validators=[DataRequired()])


def root():
    form = BuscarNoticiaForm()
    camp = Campanha.query.order_by(Campanha.id.desc()).all()
    notc = Noticia.query.order_by(Noticia.id.desc()).all()
    return render_template('index.html', campanhas = camp, noticias = notc, form = form)


def buscar_info():
    form = BuscarNoticiaForm()
    busca = form.busca.data
    search = '%{}%'.format(busca)
    notc = Noticia.query.join(Noticia.tags).filter(or_(Noticia.titulo.like(search), Noticia.descricao.like(search), Tag.tag.like(search))).all()
    cam = Campanha.query.filter(Campanha.titulo.like(search)).all()

    return render_template('buscar_informacao.html', noticias = notc, campanhas = cam, form = form)

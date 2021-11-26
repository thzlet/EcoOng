from flask import render_template
#from .models import Membro
from ecoong.blueprints.campanhas.entidades import Campanha
from ecoong.blueprints.noticias.entidades import Noticia

def root():
    camp = Campanha.query.all()
    notc = Noticia.query.all()
    return render_template('index.html', campanhas = camp, noticias = notc)
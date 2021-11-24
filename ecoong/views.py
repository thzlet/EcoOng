from flask import render_template
#from .models import Membro
from ecoong.blueprints.campanhas.entidades import Campanha

def root():
    camp = Campanha.query.all()
    return render_template('index.html', campanhass = camp)
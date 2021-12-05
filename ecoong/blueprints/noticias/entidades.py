from ecoong.ext.database import db
from datetime import datetime

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    datahora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    descricao = db.Column(db.String(300), nullable=False)

    img_not = db.Column(db.String(100), default='img_not_padrao.png')

    membro_id = db.Column(db.Integer, db.ForeignKey('membro.id'))

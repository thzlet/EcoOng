from ecoong.ext.database import db

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(15), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)

    img_not = db.Column(db.String(100), default='img_not_padrao.png')

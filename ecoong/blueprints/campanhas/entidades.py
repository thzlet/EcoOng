from ecoong.ext.database import db

class Campanha(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)

    img_cam = db.Column(db.String(100), default='img_padrao.png')

    membro_id = db.Column(db.Integer, db.ForeignKey('membro.id'))
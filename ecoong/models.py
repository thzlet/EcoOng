from ecoong.ext.database import db

class Membro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.Integer, default=0)
    idade = db.Column(db.Integer, default=0)
from ecoong.ext.database import db
from ecoong.ext.login import login
from flask_login import UserMixin

class Membro(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    telefone = db.Column(db.String(20), nullable=False)
    idade = db.Column(db.Integer, default=0)

@login.user_loader
def load_membros(id):
    return Membro.query.get(id)

from ecoong.ext.database import db
from datetime import datetime


noticiatag = db.Table('noticiatag',
    db.Column('noticia_id', db.Integer, db.ForeignKey('noticia.id', ondelete="cascade"), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete="cascade"), primary_key=True)
    )


class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    datahora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    descricao = db.Column(db.String(300), nullable=False)

    img_not = db.Column(db.String(100), default='img_not_padrao.png')

    membro_id = db.Column(db.Integer, db.ForeignKey('membro.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))

    tags = db.relationship('Tag', secondary=noticiatag, backref='noticias', cascade="all, delete" )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tag = db.Column(db.String(50), unique=True, nullable=False)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    categoria = db.Column(db.String(50), unique=True, nullable=False)

    noticia = db.relationship('Noticia', backref='categoria', lazy=True)


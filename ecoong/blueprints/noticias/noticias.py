import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
from ..noticias.entidades import Noticia, Tag, Categoria
from ecoong.models import Membro
from flask_login import current_user, login_required
from ecoong.ext.database import db
from ... import create_app
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import or_


bp = Blueprint('noticias', __name__, static_folder='static_not', template_folder='templates_not', url_prefix='/noticias')


FORMATOS_PERMITIDOS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FORMATOS_PERMITIDOS


@bp.route('/noticias')
def noticias_page():
    notc = Noticia.query.order_by(Noticia.id.desc()).all()
    cincoNotc = Noticia.query.all()
    return render_template('noticias/noticia.html', noticias = notc, cincoNoticias = cincoNotc)


@bp.route('/detalhe_not/<id>')
def detalhe_not_page(id):
    notc = Noticia.query.get(id)
    cate = Categoria.query.all()
    return render_template('noticias/detalhe_noticia.html', noticia = notc, categorias = cate)


@bp.route('/cad_noticia', methods=['GET', 'POST'])
def cadastrar_not():
    if request.method == 'POST':
        noticia = Noticia()
        noticia.titulo = request.form['titulo']
        noticia.autor = request.form['nome']
        noticia.descricao = request.form['des']
        foto = request.files['img']

        diferenca = timedelta(hours=-3)
        agora_brasil = datetime.utcnow() + diferenca
        noticia.datahora = agora_brasil

        noticia.membro_id = Membro.query.get(current_user.id).id

        current_user.noticia.append(noticia)
        db.session.commit()

        categoria_usuario = request.form['categoria']
        noticia.categoria_id = Categoria.query.filter_by(id = int(categoria_usuario)).first().id
        db.session.commit()

        tags_usuario = request.form['tags']
        tags_usuario = tags_usuario.split(',')



        for tag_usuario in tags_usuario:
            if Tag.query.filter_by(tag=tag_usuario).first() is None:
                nova_tag = Tag()
                nova_tag.tag = tag_usuario
                db.session.add(nova_tag)
                db.session.commit()

                noticia.tags.append(nova_tag)
                db.session.commit()
            else:
                jatemtag = Tag.query.filter_by(tag=tag_usuario).first()
                noticia.tags.append(jatemtag)
                db.session.commit()

        if foto and allowed_file(foto.filename):
            filename =  secure_filename(foto.filename)
            filename = filename.split('.')
            filename = f'noticia_{noticia.id}.{filename[1]}'
            noticia.img_not = filename

            app = create_app()
            foto.save(os.path.join(app.config['UPLOAD_NOTICIA'], filename))

            current_user.noticia.append(noticia)
            db.session.commit()

            flash('Notícia publicada')
            return redirect(url_for('noticias.noticias_page'))

        else:
            flash("Apenas extensões 'png', 'jpg', 'jpeg'!")
            return redirect(url_for('noticias.cadastrar_not'))


    now = str(datetime.utcnow()).split(' ')[0]
    return render_template('noticias/cadastrar_noticia.html', now=now)


@bp.get('/imagem/<nome>')
def imagens(nome):
    app = create_app()
    return send_from_directory(app.config['UPLOAD_NOTICIA'], nome)


#remover noticia
@bp.route('/remover/<id>', methods=['GET', 'POST'])
@login_required
def remover_not(id):
    noticia = Noticia.query.get(id)
    if noticia.img_not == 'img_not_padrao.png':
        db.session.delete(noticia)
        db.session.commit()

        flash('Notícia apagada!')

        return redirect(url_for('membros.historico'))

    else:
        app = create_app()
        os.remove(os.path.join(app.config['UPLOAD_NOTICIA'], noticia.img_not))

        db.session.delete(noticia)
        db.session.commit()

        flash('Notícia apagada!')

        return redirect(url_for('membros.historico'))


#editar noticia
@bp.route('/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar_not(id):

    if request.method == 'POST':
        noticia = Noticia.query.get(id)
        noticia.titulo = request.form['titulo']
        noticia.autor = request.form['nome']
        descricao = request.form['des']
        noticia.membro_id = current_user.id
        if descricao != '':
            noticia.descricao = descricao

        categoria_usuario = request.form['categoria']
        noticia.categoria_id = Categoria.query.filter_by(id = int(categoria_usuario)).first().id

        # Documentação de referência:
        # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#deleting-rows-from-the-many-to-many-table

        for tag in noticia.tags:
            noticia.tags.remove(tag)

        tags_usuario = request.form['tags']
        tags_usuario = tags_usuario.split(',')

        for tag_usuario in tags_usuario:
            if Tag.query.filter_by(tag=tag_usuario).first() is None:
                nova_tag = Tag()
                nova_tag.tag = tag_usuario

                noticia.tags.append(nova_tag)

            else:
                jatemtag = Tag.query.filter_by(tag=tag_usuario).first()
                noticia.tags.append(jatemtag)

        if 'img' in request.files:
            foto = request.files['img']

            if foto:
                if allowed_file(foto.filename):
                    filename =  secure_filename(foto.filename)
                    filename = filename.split('.')
                    filename = f'noticia_{noticia.id}.{filename[1]}'
                    noticia.img_not = filename

                    app = create_app()
                    foto.save(os.path.join(app.config['UPLOAD_NOTICIA'], filename))

                else:
                    flash("Apenas extensões 'png', 'jpg', 'jpeg'!")
                    return redirect(url_for('membros.historico'))

        current_user.noticia.append(noticia)
        db.session.commit()

        flash('Notícia atualizada')

        return redirect(url_for('membros.historico'))

    noticia = Noticia.query.get(id)
    string_tags = ''
    for tag in noticia.tags:
        string_tags = f'{string_tags},{tag.tag}'
    string_tags = string_tags[1:]

    categorias = Categoria.query.all()
    for categoria in categorias:
        if noticia.categoria_id == categoria.id:
            id_categ = categoria.id
            nome_categ = categoria.categoria

    return render_template('noticias/editar_noticia.html', noticia = noticia, categorias = categorias, id_categ = id_categ, nome_categ = nome_categ, string_tags = string_tags)


#buscar noticia
@bp.post('/busca')
def buscar_not():
    busca = request.form['busca']
    search = '%{}%'.format(busca)
    notc = Noticia.query.join(Noticia.tags).filter(or_(Noticia.titulo.like(search), Noticia.descricao.like(search), Tag.tag.like(search))).all()

    return render_template('noticias/exibir_noticias_buscada.html', noticias = notc)


def init_app(app):
    app.register_blueprint(bp)

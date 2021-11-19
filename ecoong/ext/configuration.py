import os
from typing import NoReturn

from dynaconf import FlaskDynaconf
from flask import Flask


def init_app(app: Flask) -> NoReturn:
    '''
    Use the FlaskDynaconf class as the configuration manager, environment variables and Flask extensions initializer.
     Args:
         app: Flask main instance
         '''
    FlaskDynaconf(app, instance_relative_config=True, SETTINGS_FILE=[os.path.join(app.instance_path, 'settings.toml')])
    app.config.load_extensions()
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path,'uploads')
    app.config['UPLOAD_NOTICIA'] = os.path.join(app.instance_path,'uploads','img_noticia')
    app.config['UPLOAD_PERFIL'] = os.path.join(app.instance_path,'uploads','img_perfil')
    app.config['UPLOAD_CAMPANHA'] = os.path.join(app.instance_path,'uploads','img_campanha')
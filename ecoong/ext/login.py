from flask_login import LoginManager
from typing import NoReturn
from flask import Flask

login = LoginManager()

def init_app(app : Flask) -> NoReturn:
    login.init_app(app)

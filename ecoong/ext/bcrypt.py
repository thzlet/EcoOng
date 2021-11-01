from flask_bcrypt import Bcrypt
from typing import NoReturn
from flask import Flask

bcrypt = Bcrypt()

def init_app(app : Flask) -> NoReturn:
    bcrypt.init_app(app)

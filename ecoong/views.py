from flask import render_template
from .models import Membro

def root():
    return render_template('index.html')
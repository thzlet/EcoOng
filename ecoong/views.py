from flask import render_template
from .models import Example

def root():
    return render_template('index.html')
from flask import Flask, render_template
app = Flask(__name__)
app.debug = True
@app.route('/')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

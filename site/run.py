from flask import Flask, render_template, redirect, request, flash
app = Flask(__name__)

app.secret_key = '120302'

app.debug = True

usuarios = []

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/cadastro')
def cadastro_page():
    return render_template('cadastro.html')

@app.post('/novocadastro')
def cadastrar_page():
    id_nv = len(usuarios)+1
    nome_nv = request.form['nome']
    email_nv = request.form['email']
    senha_nv = request.form['senha']
    tel_nv = request.form['tel']
    idade_nv = request.form['idade']

    novo_usuario = {
        'id': id_nv,
        'nome': nome_nv,
        'email': email_nv,
        'senha': senha_nv,
        'telefone': tel_nv,
        'idade': idade_nv
        }
    usuarios.append(novo_usuario)

    flash('BEM VINDO :)')

    return redirect('/home')


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.post('/entrar')
def entrar_page():
    email_l = request.form['email']
    senha_l = request.form['senha']
    res = None
    for usuario in usuarios:
        if email_l == usuario['email'] and senha_l == usuario['senha']:
            res = True
        else:
            res = False

    if res == True:
        flash('Logado com sucesso!!')
        return redirect('/home')
    else:
        flash('Algo deu errado :(  tente novamente!')
        return redirect('/home')

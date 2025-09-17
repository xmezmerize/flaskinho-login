from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import Usuario
import hashlib, os


# configs 
app = Flask(__name__) 
app.secret_key = os.environ.get("SECRET_KEY", "dev")
lm = LoginManager(app) 
lm.login_view = 'login' 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db" 
db.init_app(app) 

def hash_senha(txt): 
    hash_obj = hashlib.sha256(txt.encode('utf-8')) 
    return hash_obj.hexdigest() 

@lm.user_loader
def user_loader(id):
    return db.session.get(Usuario, int(id))


# read 
@app.route("/") 
def home(): 
    return render_template('home.html') 

# cadastro
@app.route("/cadastro", methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('cadastro.html')

    # POST
    nome = request.form.get('nomeForm')
    senha = request.form.get('senhaForm')
    email = request.form.get('emailForm')

    # validação de campos
    if not nome or not senha or not email:
        flash("Preencha todos os campos!", "error")
        return redirect(url_for('registrar'))

    # checar duplicidade de e-mail
    existente = Usuario.query.filter_by(email=email).first()
    if existente:
        flash("E-mail já cadastrado. Tente outro.", "error")
        return redirect(url_for('registrar'))

    # gerar hash da senha
    senha_hash = generate_password_hash(senha)

    # criar novo usuário
    novo_usuario = Usuario(nome=nome, senha=senha_hash, email=email)
    db.session.add(novo_usuario)
    db.session.commit()

    # login automático
    login_user(novo_usuario)
    flash("Cadastro realizado com sucesso!", "success")

    return redirect(url_for('home'))
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # POST
    email = request.form.get('emailForm')
    senha = request.form.get('senhaForm')

    # buscar usuário pelo e-mail
    user = Usuario.query.filter_by(email=email).first()

    # validar usuário e senha
    if not user or not check_password_hash(user.senha, senha):
        flash("Email ou senha incorretos.", "error")
        return redirect(url_for('login'))

    # login
    login_user(user)
    flash("Login realizado com sucesso!", "success")
    return redirect(url_for('home'))

# logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for('home'))


if __name__ == '__main__': 
    with app.app_context(): 
        db.create_all() 
    app.run(debug=True)
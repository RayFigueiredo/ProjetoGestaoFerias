from flask import render_template, redirect, url_for, flash
from ProjetoCRUD import app
from ProjetoCRUD.Models import Usuario, bcrypt, db
from flask_login import login_required, login_user, logout_user, current_user
from ProjetoCRUD.forms import FormLogin, FormCriarConta


@app.route("/tela_login", methods=["GET", "POST"])
def tela_login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for('home'))

    return render_template('tela_login.html', form=form_login)


@app.route("/criar_conta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        flash("Conta Criada com sucesso!", "success")
        return redirect(url_for('tela_login'))

    return render_template('criar_conta.html', form=form_criarconta)


@app.route("/")
@login_required
def home():

    return render_template('index.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('tela_login'))

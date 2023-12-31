from flask import render_template, redirect, url_for, flash
from ProjetoCRUD import app
from ProjetoCRUD.Models import Usuario, bcrypt, db
from flask_login import login_required, login_user, logout_user
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
        email = form_criarconta.email.data
        usuario_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:
            flash("E-mail já cadastrado, faça login para continuar", "error")
            return redirect(url_for('criar_conta'))

        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=email, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        flash("Conta Criada com sucesso! " "Faça Login para continuar", "success")
        return redirect(url_for('criar_conta'))

    return render_template('criar_conta.html', form=form_criarconta)


@app.route("/")
@login_required
def home():

    return render_template('index.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('tela_login'))

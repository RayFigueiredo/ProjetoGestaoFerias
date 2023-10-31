from flask import render_template
from ProjetoCRUD import app

app.secret_key = '12345678'  # Defina uma chave secreta única aqui


@app.route("/")
def home():

    return render_template('index.html')

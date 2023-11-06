from flask import Flask

app = Flask(__name__, template_folder='templates')

from ProjetoCRUD.Models import db, Departamento, Ferias, Funcionario
from ProjetoCRUD.BackEnd.ModuloFerias import (GerarRelatorio, ViewCadastrarFerias,
                                              ViewConsultaFerias, ViewDeletarFerias,
                                              ViewEditarFerias)
from ProjetoCRUD.BackEnd.ModuloDpto import ViewCRUDDpto
from ProjetoCRUD.BackEnd.ModuloFunc import ViewCRUDFunc
from ProjetoCRUD.BackEnd import TelaInicial

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mack#2351@localhost/bdferias'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:945bo1bQFfqgqWY3NtLH@containers-us-west-87.railway.app:6810/railway'
app.config["SECRET_KEY"] = "15b6688e71b5def74f934ded82bddc76"
# Inicialize o aplicativo com a extensão SQLAlchemy

db.init_app(app)


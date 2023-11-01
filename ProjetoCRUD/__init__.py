from flask import Flask

app = Flask(__name__, template_folder='templates')

from ProjetoCRUD.BluePrints.Classes import db, Departamento, Ferias, Funcionario
from ProjetoCRUD.BluePrints.ModuloFerias import (GerarRelatorio, ViewCadastrarFerias,
                                                 ViewConsultaFerias, ViewDeletarFerias,
                                                 ViewEditarFerias)
from ProjetoCRUD.BluePrints.ModuloDpto import ViewCRUDDpto
from ProjetoCRUD.BluePrints.ModuloFunc import ViewCRUDFunc

from ProjetoCRUD.BluePrints import TelaInicial

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mack#2351@localhost/bdferias'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:945bo1bQFfqgqWY3NtLH@containers-us-west-87.railway.app:6810/railway'
# Inicialize o aplicativo com a extensão SQLAlchemy
db.init_app(app)

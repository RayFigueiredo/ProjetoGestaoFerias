from ProjetoCRUD import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "tela_login"


@login_manager.user_loader
def load_usuario(id_usuario):

    return Usuario.query.get(int(id_usuario))


class Usuario(db.Model, UserMixin):
    __tablename__ = 'tb_user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)


class Funcionario(db.Model):
    __tablename__ = 'tb_func'

    mat = db.Column(db.String(7), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    dpto_id = db.Column(db.Integer, ForeignKey('tb_dpto.id'), nullable=False)

    # Defina o relacionamento com a tabela tb_dpto
    dpto = db.relationship('Departamento', backref='funcionarios')


class Ferias(db.Model):
    __tablename__ = 'tb_ferias'

    id = db.Column(db.Integer, primary_key=True)
    func_mat = db.Column(db.String(7), ForeignKey('tb_func.mat'), nullable=False)
    func_nome = db.Column(db.String(255), ForeignKey('tb_func.nome'), nullable=False)
    dpto_nome = db.Column(db.String(255), ForeignKey('tb_dpto.nome'), nullable=False)
    data_ini = db.Column(db.Date, nullable=False)
    qtd_dias = db.Column(db.Integer, nullable=False)

    # Defina o relacionamento com a tabela tb_func
    funcionario = db.relationship(
        'Funcionario',
        primaryjoin="and_(Ferias.func_mat==Funcionario.mat, Ferias.func_nome==Funcionario.nome)",
        backref='ferias'
    )
    departamento = db.relationship('Departamento', foreign_keys=[dpto_nome], backref='ferias')


class Departamento(db.Model):
    __tablename__ = 'tb_dpto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)

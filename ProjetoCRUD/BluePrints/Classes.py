from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


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

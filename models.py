from utils import db
from flask_login import UserMixin
import enum


class UserType(enum.Enum):
    L = "L"
    V = "V"


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))
    user_type = db.Column(db.Enum(UserType))
    admin = db.Column(db.Boolean)

    rs_usuario_lar = db.relationship('Lar', cascade="all,delete", backref="usuario_lar")
    rs_usuario_volunteer = db.relationship('Voluntario', cascade="all,delete", backref="usuario_voluntario")
    rs_usuario_visit = db.relationship('Visita', cascade="all,delete", backref="usuario_visita")

    def __init__(self, email, senha, admin, user_type):
        self.email = email
        self.senha = senha
        self.admin = admin
        self.user_type = user_type

    def __repr__(self):
        return f"usuario('{self.email}, {self.senha}, {self.admin}, {self.user_type}')"


class Doacao(db.Model):
    __tablename__ = 'doacao'
    id = db.Column(db.Integer, primary_key=True)
    larNome = db.Column(db.String(100))
    valor = db.Column(db.Numeric(precision=2))
    nomeDoador = db.Column(db.String(100))

    def __init__(self, larNome, valor, nomeDoador):
        self.larNome = larNome
        self.valor = valor
        self.nomeDoador = nomeDoador

    def __repr__(self):
        return f"doacao('{self.id}, {self.larNome}, {self.valor}, {self.nomeDoador}')"


class Voluntario(db.Model):
    __tablename__ = 'voluntario'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
    nome = db.Column(db.String(100))

    usuario = db.relationship('Usuario', foreign_keys=id_usuario)

    def __init__(self, id_usuario, nome):
        self.id_usuario = id_usuario
        self.nome = nome

    def __repr__(self):
        return f"voluntario('{self.nome}')"


class Lar(db.Model):
    __tablename__ = 'lar_de_idosos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
    nome = db.Column(db.String(100))
    pix = db.Column(db.String(100))
    cep = db.Column(db.String(100))
    rs_lar_visit = db.relationship('Visita', cascade="all,delete", backref="lar_visita")

    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.nome = None
        self.pix = ''
        self.cep = ''

    def __repr__(self):
        return f"Lar_de_idosos('{self.nome}')"


class Visita(db.Model):
    __tablename__ = 'visita'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_lar = db.Column(db.Integer, db.ForeignKey('lar_de_idosos.id'))
    nome_voluntario = db.Column(db.String(100))
    nome_lar = db.Column(db.String(100))
    data = db.Column(db.Date)
    hora = db.Column(db.Time)
    motivo = db.Column(db.String(500))

    def __init__(self, id_usuario, id_lar, nome_voluntario, nome_lar, data, hora, motivo):
        self.id_usuario = id_usuario
        self.id_lar = id_lar
        self.nome_voluntario = nome_voluntario
        self.nome_lar = nome_lar
        self.data = data
        self.hora = hora
        self.motivo = motivo

    def __repr__(self):
        return f"visita('{self.nome_voluntario}, {self.nome_lar}, {self.data}, {self.hora}, {self.motivo}')"

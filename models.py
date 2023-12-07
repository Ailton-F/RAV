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

    rs_usuario_lar = db.relationship('Lar', cascade="all,delete", backref="usuario_lar")
    rs_usuario_volunteer = db.relationship('Voluntario', cascade="all,delete", backref="usuario_voluntario")

    def __init__(self, email, senha, user_type):
        self.email = email
        self.senha = senha
        self.user_type = user_type

    def __repr__(self):
        return f"usuario('{self.email}, {self.senha}, {self.user_type}')"


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
    telefone = db.Column(db.String(45))
    usuario = db.relationship('Usuario', foreign_keys=id_usuario)
    rs_voluntario_visit = db.relationship('Visita', cascade="all,delete", backref="voluntario_visita")

    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.nome = ''

    def __repr__(self):
        return f"voluntario('{self.nome}')"


class Lar(db.Model):
    __tablename__ = 'lar_de_idosos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
    nome = db.Column(db.String(100))
    pix = db.Column(db.String(100))
    cep = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    telefone = db.Column(db.String(100))
    principais_necessidades = db.Column(db.String(140))
    rs_lar_visit = db.relationship('Visita', cascade="all,delete", backref="lar_visita")

    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.nome = None
        self.pix = ''
        self.cep = ''
        self.instagram = ''
        self.telefone = ''
        self.principais_necessidades = ''

    def __repr__(self):
        return f"Lar_de_idosos('{self.nome}')"


class Visita(db.Model):
    __tablename__ = 'visita'
    id = db.Column(db.Integer, primary_key=True)
    id_voluntario = db.Column(db.Integer, db.ForeignKey('voluntario.id'))
    id_lar = db.Column(db.Integer, db.ForeignKey('lar_de_idosos.id'))
    dt_hr = db.Column(db.DateTime,)
    qnt_pessoas = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    motivo = db.Column(db.String(500))

    def __init__(self, id_voluntario, id_lar, nome_lar, dt_hr, motivo):
        self.id_usuario = id_usuario
        self.id_lar = id_lar
        self.dt_hr = dt_hr
        self.motivo = motivo

    def __repr__(self):
        return f"visita('{self.nome_lar}, {self.dt_hr}, {self.motivo}')"

from utils import db
from flask_login import UserMixin
import enum

class UserType(enum.Enum):
  A = "A"
  V = "V"
  
class Usuario(db.Model, UserMixin):
  __tablename__ = 'usuario'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100))
  senha = db.Column(db.String(100))
  cpf_cnpj = db.Column(db.String(100))
  user_type = db.Column(db.Enum(UserType))
  login_step = db.Column(db.Integer)
  admin = db.Column(db.Boolean)
  
  rs_usuario_asylum = db.relationship('Asilo', backref="usuario_asilo")
  rs_usuario_volunteer = db.relationship('Voluntario', backref="usuario_voluntario")
  rs_usuario_visit = db.relationship('Visita', backref="usuario_visita")

  def __init__(self, email, senha, admin, user_type, login_step):
    self.email = email
    self.senha = senha
    self.admin = admin
    self.user_type = user_type
    self.login_step = login_step

  def __repr__(self):
    return f"usuario('{self.email}, {self.senha}, {self.cpf_cnpj}, {self.admin}, {self.user_type}')"

class Doacao(db.Model):
  __tablename__ = 'doacao'
  id = db.Column(db.Integer, primary_key = True)
  asiloName = db.Column(db.String(100))
  valor = db.Column(db.Numeric(precision=2))
  nomeDoador = db.Column(db.String(100))

  def __init__(self, asiloName, valor, nomeDoador):
    self.asiloName = asiloName
    self.valor = valor
    self.nomeDoador = nomeDoador

  def __repr__(self):
    return f"doacao('{self.id}, {self.asiloNome}, {self.valor}, {self.nomeDoador}')"

class Voluntario(db.Model):
  __tablename__ = 'voluntario'
  id = db.Column(db.Integer, primary_key=True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
  nome = db.Column(db.String(100))
  cpf_cnpj = db.Column(db.String(100))

  usuario = db.relationship('Usuario', foreign_keys=id_usuario)

  def __init__(self, id_usuario, nome, cpf_cnpj):
    self.id_usuario = id_usuario
    self.nome = nome
    self.cpf_cnpj = cpf_cnpj

  def __repr__(self):
    return f"voluntario('{self.nome}, {self.cpf_cnpj}')"
    

class Asilo(db.Model):
  __tablename__ = 'asilo'
  id = db.Column(db.Integer, primary_key=True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
  nome = db.Column(db.String(100))
  cep = db.Column(db.String(100))
  cnpj = db.Column(db.String(100))
  rs_asylum_visit = db.relationship('Visita', backref="asylum_visita")


  def __init__(self, id_usuario, nome, cep, cnpj):
    self.nome = nome
    self.cep= cep
    self.cnpj = cnpj

  def __repr__(self):
    return f"asilo('{self.nome}, {self.cep}, {self.cnpj}')"

class Visita(db.Model):
  __tablename__ = 'visita'
  id = db.Column(db.Integer, primary_key=True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
  id_asilo = db.Column(db.Integer, db.ForeignKey('asilo.id'), unique=True)
  nome_voluntario = db.Column(db.String(100))
  nome_asilo = db.Column(db.String(100))
  data = db.Column(db.Date)
  hora = db.Column(db.Time)
  motivo = db.Column(db.String(500))


  def __init__(self, id_usuario, nome_voluntario, nome_asilo, data, hora, motivo):
    self.nome_voluntario = nome_voluntario
    self.nome_asilo= nome_asilo
    self.data= data
    self.hora= hora
    self.motivo = motivo

  def __repr__(self):
    return f"visita('{self.nome_voluntario}, {self.nome_asilo}, {self.data}, {self.hora}, {self.motivo}')"
  
  

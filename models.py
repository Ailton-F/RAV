from database import db
import enum

class UserType(enum.Enum):
  ASILO = "A"
  VOLUNTARIO = "V"
  
class Usuario(db.Model):
  __tablename__ = 'usuario'
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100))
  email = db.Column(db.String(100))
  senha = db.Column(db.String(100))
  cpf_cnpj = db.Column(db.String(100))
  user_type = db.Column(db.Enum(UserType))
  admin = db.Column(db.Boolean)

  def __init__(self, nome, email, senha, admin, user_type):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.admin = admin
    self.user_type = user_type

  def __repr__(self):
    return f"usuario('{self.nome}, {self.email}, {self.senha}, {self.cpf_cnpj}, {self.admin}, {self.user_type}')"

class Doacao(db.Model):
  __tablename__ = 'doacao'
  id = db.Column(db.Integer, primary_key = True)
  asiloName = db.Column(db.String(100))
  valor = db.Column(db.Numeric(precision=2))
  nomeDoador = db.Column(db.String(100))

  def __init__(self, id, asiloName, valor, nomeDoador):
    self.id = id
    self.asiloName = asiloName
    self.valor = valor
    self.nomeDoador = nomeDoador

  def __repr__(self):
    return f"doacao('{self.id}, {self.asiloNome}, {self.valor}, {self.nomeDoador}')"
  
  
  
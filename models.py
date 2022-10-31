from database import db

class Usuario(db.Model):
  __tablename__ = 'usuario'
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100))
  email = db.Column(db.String(100))
  senha = db.Column(db.String(100))
  cpf_cnpj = db.Column(db.String(100))

  def __init__(self, nome, email, senha, cpf_cnpj):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.cpf_cnpj = cpf_cnpj

  def __repr__(self):
    return f"usuario(''{self.nome}, {self.email}, {self.senha}, {self.cpf_cnpj}')"

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
  
  
  
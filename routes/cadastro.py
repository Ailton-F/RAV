from flask import Blueprint
from controllers import cad

cadastro_bl = Blueprint('cadastro', __name__)

#Rotas de cadastro
#Retorna a página de cadastro 
@cadastro_bl.route('/cadastro')
@cadastro_bl.route('/cadastro')
def cadastro(): 
  return cad.getCadPage()
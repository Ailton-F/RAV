from flask import Blueprint
from controllers import doacoes

donate_bl = Blueprint('donate', __name__)

#Rotas de doação
#Retorna a página de doações
@donate_bl.route('/doacoes')
def donate(): 
  return doacoes.getDoacoesPage()
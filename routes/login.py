from flask import Blueprint
from controllers import login

log_bl = Blueprint('login', __name__)

#Rotas de login
#Retorna a página de login
@log_bl.route('/login')
@log_bl.route('/login')
def log(): 
  return login.getLoginPage()
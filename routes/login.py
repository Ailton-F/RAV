from flask import Blueprint, request
from controllers import login
from utils import lm
from models import Usuario

log_bl = Blueprint('login', __name__)


#Rotas de login
#Carrega o usuário a partir do ID guardado na sessão
@lm.user_loader
def load_user(id):
    return Usuario.query.get(id)

#Retorna a página de login
@log_bl.route('/', methods=['GET', 'POST'])
def log(): return login.getLogin()

@log_bl.route('/google', methods=['POST'])
def logoogle(): return login.getGoogleLogin()

@log_bl.route('/callback')
def callbackOauth(): return login.callback()
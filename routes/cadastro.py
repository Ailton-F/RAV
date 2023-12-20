from flask import Blueprint
from controllers import cad

cadastro_bl = Blueprint('cadastro', __name__)

#Rotas de cadastro
#Retorna a página de cadastro 
@cadastro_bl.route('/')
def cadastro(): return cad.getCadPage()

@cadastro_bl.route('/google-cad', methods=["POST"])
def google(): return cad.get_google_cad()

@cadastro_bl.route('/callback')
def callback(): return cad.callback()
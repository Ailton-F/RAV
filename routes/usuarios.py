
from flask import Blueprint
from controllers import cad

users_bl = Blueprint("usuarios", __name__)

@users_bl.route('/usuarios/users_recovery')
def recovery(): return cad.recover()

@users_bl.route('/create', methods=['GET', 'POST'])
def insert(): return cad.create()
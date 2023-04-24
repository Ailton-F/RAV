from flask import Blueprint
from controllers import map

mapa_bl = Blueprint('map', __name__)

#Rota do mapa
#Retorna a página do mapa
@mapa_bl.route('/')
def mapa():
    return map.getMapPage()

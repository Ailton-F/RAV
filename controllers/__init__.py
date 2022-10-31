from .CadController import Cad
from .DoacoesController import Doacoes
from .LoginController import Login
from .MapController import Map

cad = Cad()
doacoes = Doacoes()
login = Login()
map = Map()

__all__ = ['cad',
           'doacoes',
           'login',
           'map']

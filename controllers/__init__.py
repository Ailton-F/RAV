from .CadController import Cad
from .DoacoesController import Doacoes
from .LoginController import Login
from .MapController import Map
from .UserController import User

cad = Cad()
doacoes = Doacoes()
login = Login()
map = Map()
user = User()

__all__ = ['cad',
          'doacoes',
          'login',
          'map',
          'user']

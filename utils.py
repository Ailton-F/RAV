from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from geopy.geocoders import Nominatim

lm = LoginManager()
db = SQLAlchemy()
loc = Nominatim(user_agent="myGeocoder")
ceps = [
    '59133280',
    # '59014104',
    # '59022150',
    # '59123289',
    # '59108480',
    # '59022300',
    # '59124002',
    # '59135250',
    # '59014000',
    # '59115522',
]
from flask import render_template
import folium, requests
from utils import loc, ceps

class Map:
  
  #Retorna a página do mapa
  @staticmethod
  def getMapPage():
    
    # Define the coordinates of Natal
    latitude = -5.7955
    longitude = -35.2090
    
    # Create a Folium map centered on Natal
    my_map = folium.Map(location=[latitude, longitude], zoom_start=12)

    # Get the place based on the CEP
    # for cep in ceps:
    # cep = '59014104'
    # uri = f'https://viacep.com.br/ws/{cep}/json/'
    # req = requests.get(uri)
    # dict_req = req.json()
    # bairro = dict_req['bairro']
    # rua = dict_req['logradouro']
    # uf = dict_req['uf']
    # location = loc.geocode(f'Escadaria Guanabara, Areia Preta')
    # return f'{location}'

    # folium.Marker(
    #   location=[location.latitude, location.longitude],
    #   tooltip='Lar tal tal',
    #   popup=''
    # ).add_to(my_map)
        
    iframe = my_map.get_root()._repr_html_()
    
    return render_template('mapa.html', iframe=iframe)
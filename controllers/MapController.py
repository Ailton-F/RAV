from flask import render_template
import folium

class Map:
  
  #Retorna a página do mapa
  @staticmethod
  def getMapPage():
    
    # Define the coordinates of Natal
    latitude = -5.7955
    longitude = -35.2090
    
    # Create a Folium map centered on Natal
    my_map = folium.Map(location=[latitude, longitude], zoom_start=12)
       
    iframe = my_map.get_root()._repr_html_()
    
    return render_template('mapa.html', iframe=iframe)
from flask import render_template

class Map:
  
  #Retorna a página do mapa
  @staticmethod
  def getMapPage():
    return render_template('mapa.html')
    
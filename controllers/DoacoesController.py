from flask import render_template

class Doacoes():
  
  #Retorna a página de doações
  @staticmethod
  def getDoacoesPage():
    return render_template('doacoes.html')
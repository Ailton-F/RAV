from flask import render_template

class Login():

  #Método responsável por retornar a página de login
  @staticmethod
  def getLoginPage():
    return render_template('login.html')
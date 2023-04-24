from flask import render_template, request, redirect, url_for, flash
from models import Usuario
from flask_login import login_user, current_user

class Login():
  
  #Método responsável por retornar a página de login
  @staticmethod
  def getLogin():
    if request.method == 'GET':
      return render_template('login.html')
    if request.method == 'POST':
      email = request.form.get('login-email')
      senha = request.form.get('login-password')
      user = Usuario.query.filter_by(email = email).first()

      if email == user.email and senha == user.senha:    
        login_user(user)
        return redirect('/usuarios')
      else:
        flash('Dado(s) incorreto(s)','danger')
        return redirect('/login')
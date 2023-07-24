from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user
from models import Usuario
from utils import db


class Cad():
  
  #Método responsável por retornar a página de cadastro
  @staticmethod
  def getCadPage():
    return render_template('cad.html')

  @staticmethod
  def create():
    if request.method=='GET':
      return render_template('cad.html')
  
    if request.method=='POST':
      email = request.form.get('cad-email')
      senha = request.form.get('cad-password')
      csenha = request.form.get('cad-repassword')
      admin = False
      user_type = request.form.get('tipo')
      try:
        usuario = Usuario(email, senha, admin, user_type, 1)
        usuario_existe = Usuario.query.filter_by(email = email).first()

        if usuario_existe and usuario.email in usuario_existe.email:
          flash('Email já cadastrado', 'danger')
          return redirect('/cadastro')
          
        if senha != csenha:
          flash('Senhas diferentes', 'danger')
          return redirect('/cadastro')

        db.session.add(usuario)
        db.session.commit()
        
        login_user(usuario)
      except:
        flash('Erro interno, por favor aguarde', 'danger')
        return redirect('/cadastro')
      
      return redirect('/usuarios/user_config')  
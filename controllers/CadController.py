from flask import render_template, request, redirect, flash
from models import Usuario
from database import db


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
      nome = request.form.get('nome')
      email = request.form.get('email')
      senha = request.form.get('senha')
      admin = False
      user_type = request.form.get('tipo')
      usuario = Usuario(nome, email, senha, admin, user_type)
      
      db.session.add(usuario)
      db.session.commit()
      flash('Dados cadastrados com sucesso!', 'success')
      return redirect('/user-config')


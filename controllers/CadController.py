from flask import render_template, request, redirect, flash, url_for
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
      cpf_cnpj = request.form.get('cpf_cnpj')
      usuario = Usuario(nome, email, senha, cpf_cnpj)
      db.session.add(usuario)
      db.session.commit()
      flash('Dados cadastrados com sucesso!', 'success')
      return redirect('/user-config')


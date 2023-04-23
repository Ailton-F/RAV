from flask import render_template, redirect, flash, session, request
from models import Usuario, Voluntario, Visita
from utils import db
from flask_login import current_user, logout_user

class User():

  #retorna a página de usuário
  @staticmethod
  def getHome():
    u_id = current_user.id
    user = db.session.query(Voluntario.nome).join(Usuario, Voluntario.id_usuario == u_id).first()
    return render_template('user/home.html', user=user)
    
  #retorna a página de administradores
  @staticmethod
  def getAdminPage():
    usuarios = Usuario.query.all()
    if current_user.admin:
      return render_template('admin.html', usuarios=usuarios)
    else:
      flash('Você não tem autorização para acessar', 'danger')
      return redirect('/usuarios')

  #Encerra sessão do usuário
  @staticmethod
  def logUserOff():
    logout_user()
    if session.get('was_once_logged_in'):
        # prevent flashing automatically logged out message
        del session['was_once_logged_in']
      
    flash('Conta deslogada', 'success')
    return redirect('/login')

  #Deleta o usuário do banco de dados
  @staticmethod
  def deleteUser(id):
    if current_user.id != id and not current_user.admin:
      flash('Você não tem as permissões necessárias para realizar essa ação', 'danger')
      return redirect('/usuarios')
    
    user = Usuario.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    if current_user.admin:
      flash('Usuário deletado com sucesso!', 'success')
      return '/usuarios/admin'
    else:
      flash('Sua conta foi deletada com sucesso!', 'success')
      return '/'

  #GET:Carrega a página de edição de usuário, POST:Edita o usuário
  @staticmethod
  def editUser(id):
    if current_user.id != id and not current_user.admin:
      flash('Você não tem as permissões necessárias para realizar essa ação', 'danger')
      return redirect('/usuarios')
      
    user = Usuario.query.filter_by(id=id).first()
    if request.method == 'GET':
      return render_template('user/edit.html', user=user)

    elif request.method == 'POST':
      email = request.form.get('edit-email')
      senha = request.form.get('edit-pass')
      csenha = request.form.get('confirm-edit-pass')
      
      if senha != csenha:
        flash('As senhas não coincidem', 'danger')
        return redirect(f'/usuarios/edit/{user.id}')

      user.email = email
      user.senha = senha

      db.session.add(user)
      db.session.commit()

      flash('Dados alterados com sucesso', 'success')
      return redirect('/usuarios/admin')

  #Retorna a página de perfil do usuário
  @staticmethod
  def getProfilePage():
    user = Usuario.query.filter_by(id=current_user.id).first()
    return render_template('user/profile.html', user=user)

  #Retorna a página de configuração de usuário do tipo voluntário
  @staticmethod
  def getVolunteerConfigPage():
    if request.method == 'GET':
      return render_template('user/config.html')

    name = request.form.get('user-name')
    cpf_cnpj = request.form.get('cpf-cnpj')
    print(current_user)
    id_user = current_user.id

    volunteer = Voluntario(id_user, name, cpf_cnpj)
    db.session.add(volunteer)
    db.session.commit()

    return redirect('/')
  #Retorna a página de configuração de usuário do tipo asylum
  @staticmethod
  def getAsylumConfigPage():
    return render_template('user/asylum_config.html')

  #retorna a página de visitas
  @staticmethod
  def getVisitHomePage():
    asilos = Usuario.query.filter_by(user_type="A").limit(8)
    return render_template('visit/home.html', asilos=asilos)
    
  #Retorna a página do chat
  @staticmethod
  def getChatPage():
    return render_template('user/chat.html',user=current_user)

  #Retorna o template das mensagens
  @staticmethod
  def getMsgTemplate():
    return render_template('msg.html')

  #Retorna a página para marcar visitas
  @staticmethod
  def getBookVisitPage():
    if request.method == "GET":
      return render_template('visit/book.html')

    name = request.form.get('name')
    asylum_name = request.form.get('asylum-name')
    visit_date = request.form.get('visit-date')
    visit_hour = request.form.get('visit-hour')
    visit_reason = request.form.get('visit-reason')
    id_usuario = current_user.id
    visit = Visita(id_usuario, name, asylum_name, visit_date, visit_hour, visit_reason)
    
    db.session.add(visit)
    db.session.commit()
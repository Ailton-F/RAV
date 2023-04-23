from flask import render_template, redirect, flash, session, request
from models import Usuario, Voluntario, Visita, Asilo
from utils import db
from flask_login import current_user, logout_user
from datetime import datetime


class User():

    #retorna a página de usuário
    @staticmethod
    def getHome():
        u_id = current_user.id
        if current_user.user_type._value_ == 'A':
            user = db.session.query(Asilo.nome).join(
                Usuario, Asilo.id_usuario == u_id).first()
        else:
            user = db.session.query(Voluntario.nome).join(
                Usuario, Voluntario.id_usuario == u_id).first()
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
            flash(
                'Você não tem as permissões necessárias para realizar essa ação',
                'danger')
            return redirect('/usuarios')

        user = Usuario.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

        if current_user.admin:
            flash('Usuário deletado com sucesso!', 'success')
            return redirect('/usuarios/admin')
        else:
            flash('Sua conta foi deletada com sucesso!', 'success')
            return '/'

    #GET:Carrega a página de edição de usuário, POST:Edita o usuário

    @staticmethod
    def editUser(id):
        if current_user.id != id and not current_user.admin:
            flash(
                'Você não tem as permissões necessárias para realizar essa ação',
                'danger')
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
            return redirect('/usuarios')

    #Retorna a página de perfil do usuário

    @staticmethod
    def getProfilePage():
      user = Usuario.query.filter_by(id=current_user.id).first()
      if current_user.user_type._value_ == 'A':
        userType = Asilo.query.filter_by(id_usuario=user.id).first()
      else: userType = Voluntario.query.filter_by(id_usuario=user.id).first()
      return render_template('user/profile.html', user=user, userType=userType)

    #Retorna a página de configuração de usuário do tipo voluntário

    @staticmethod
    def getVolunteerConfigPage():
        if request.method == 'GET':
            return render_template('user/config.html')

        name = request.form.get('user-name')
        cpf_cnpj = request.form.get('cpf-cnpj')
        id_user = current_user.id

        if current_user.user_type._value_ == 'A':
            user = Asilo(id_user, name, cpf_cnpj)
        else:
            user = Voluntario(id_user, name, cpf_cnpj)

        db.session.add(user)
        db.session.commit()

        return redirect('/')

    #Retorna a página de configuração de usuário do tipo asylum

    @staticmethod
    def getAsylumConfigPage():
        return render_template('user/asylum_config.html')

    #retorna a página de visitas

    @staticmethod
    def getVisitHomePage():

        asilos = db.session.query(Asilo.id, Asilo.nome).limit(8)
        if current_user.user_type._value_ == 'V':
            rs_visits = Visita.query.filter_by(id_usuario=current_user.id)
        else:
            rs_asilo = Asilo.query.filter_by(
                id_usuario=current_user.id).first()
            rs_visits = Visita.query.filter_by(nome_asilo=rs_asilo.nome)

        return render_template('visit/home.html',
                               asilos=asilos,
                               visitas=rs_visits)

    #Retorna a página do chat

    @staticmethod
    def getChatPage():
        return render_template('user/chat.html', user=current_user)

    #Retorna o template das mensagens

    @staticmethod
    def getMsgTemplate():
        return render_template('msg.html')

    #Retorna a página para marcar visitas

    @staticmethod
    def getBookVisitPage(request_id):

        asilo = Asilo.query.filter_by(id=request_id).first()

        if request.method == "GET":

            return render_template('visit/book.html', asilo=asilo)

        id_usuario = current_user.id
        asylum_id = asilo.id
        volunteer_name = request.form.get('name')
        asylum_name = asilo.nome

        #Faz a formatação da data
        visit_date = request.form.get('visit-date')
        date = map(lambda item: int(item), visit_date.split('-'))
        date = list(date)
        fdate = datetime(date[0], date[1], date[2])
        visit_date = fdate.date()

        #Faz a formatação da hora
        visit_hour = request.form.get('visit-hour')
        visit_hour = map(lambda item: int(item), visit_hour.split(':'))
        visit_hour = list(visit_hour)
        fhour = datetime(1999, 1, 1, visit_hour[0], visit_hour[1])
        visit_hour = fhour.time()

        visit_reason = request.form.get('visit-reason')

        visit = Visita(id_usuario, asylum_id, volunteer_name, asylum_name,
                       visit_date, visit_hour, visit_reason)

        db.session.add(visit)
        db.session.commit()

        flash('Visita marcada com sucesso!', 'success')
        return redirect('/usuarios/visit')

    #Retorna o dashboard das visitas

    @staticmethod
    def getDashboard():
        if current_user.user_type._value_ == 'V':
            rs_visits = Visita.query.filter_by(id_usuario=current_user.id)
        else:
            rs_asilo = Asilo.query.filter_by(
                id_usuario=current_user.id).first()
            rs_visits = Visita.query.filter_by(nome_asilo=rs_asilo.nome)
        return render_template('visit/dashboard.html', visitas=rs_visits)

    #Deleta a visita do banco de dados

    @staticmethod
    def deleteVisitLink(id):
        visit = Visita.query.filter_by(id=id).first()
        db.session.delete(visit)
        db.session.commit()

        flash('Visita deletada com sucesso!', 'success')
        return redirect('/usuarios/dashboard')

    #GET: Retorna a página de edição da visita, POST: edita a visita

    @staticmethod
    def editVisitPage(id):
        visit = Visita.query.filter_by(id=id).first()
        if request.method == "GET":
            return render_template('visit/edit.html', visit=visit)

        #Faz a formatação da data
        visit_date = request.form.get('visit-date')
        date = map(lambda item: int(item), visit_date.split('-'))
        date = list(date)
        fdate = datetime(int(date[0]), int(date[1]), int(date[2]))
        visit_date = fdate.date()

        #Faz a formatação da hora
        visit_hour = request.form.get('visit-hour')
        visit_hour = map(lambda item: int(item), visit_hour.split(':'))
        visit_hour = list(visit_hour)
        fhour = datetime(1999, 1, 1, visit_hour[0], visit_hour[1])
        visit_hour = fhour.time()

        visit.data = visit_date
        visit.hora = visit_hour
        visit.nome_voluntario = request.form.get('name')
        visit.motivo = request.form.get('visit-reason')

        db.session.add(visit)
        db.session.commit()

        flash('Visita editada com sucesso!', 'success')
        return redirect('/usuarios/dashboard')

    @staticmethod
    def getAsylumProfile(id):
        asylum = Asilo.query.filter_by(id=id).first()
        return f'ID: {asylum.id}<br> NOME: {asylum.nome}<br> LINK: <a href="/usuarios/book/{asylum.id}">Marcar visita</a>'

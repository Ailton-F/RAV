from flask import render_template, redirect, flash, session, request
from models import Usuario, Voluntario, Visita, Lar
from utils import db
from flask_login import current_user, logout_user
from datetime import datetime


class User():

    # retorna a página de usuário
    @staticmethod
    def getHome():
        if "id_info" not in session:
            u_id = current_user.id
            if current_user.user_type._value_ == 'A':
                user = db.session.query(Lar.nome).join(
                    Usuario, Lar.id_usuario == u_id).first()
            else:
                user = db.session.query(Voluntario.nome).join(
                    Usuario, Voluntario.id_usuario == u_id).first()

        else:
            user = {}
            user['nome'] = session['id_info']['given_name']

        return render_template('user/home.html', user=user)

    # retorna a página de administradores

    @staticmethod
    def getAdminPage():
        usuarios = Usuario.query.all()
        if current_user.admin:
            return render_template('admin.html', usuarios=usuarios)
        else:
            flash('Você não tem autorização para acessar', 'danger')
            return redirect('/usuarios')

    # Encerra sessão do usuário

    @staticmethod
    def logUserOff():
        session.clear()
        logout_user()
        if session.get('was_once_logged_in'):
            # prevent flashing automatically logged out message
            del session['was_once_logged_in']

        flash('Conta deslogada', 'success')
        return redirect('/login')

    # Deleta o usuário do banco de dados

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

    # GET:Carrega a página de edição de usuário, POST:Edita o usuário

    @staticmethod
    def editUser(id):
        if current_user.id != id and not current_user.admin:
            flash(
                'Você não tem as permissões necessárias para realizar essa ação',
                'danger')
            return redirect('/usuarios')

        user = Usuario.query.filter_by(id=id).first()
        if user.user_type._value_ == 'V':
            usertype = Voluntario.query.filter_by(id_usuario=user.id).first()
        else:
            usertype = Lar.query.filter_by(id_usuario=user.id).first()
        if request.method == 'GET':
            return render_template('user/edit.html', user=user, usertype=usertype)

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

    # Retorna a página de perfil do usuário

    @staticmethod
    def getProfilePage():
        u_id = current_user.id
        if current_user.user_type._value_ == 'L':
            userName = db.session.query(Lar.nome).join(
                Usuario, Lar.id_usuario == u_id).first()
        else:
            userName = db.session.query(Voluntario.nome).join(
                Usuario, Voluntario.id_usuario == u_id).first()

        return render_template('user/profile.html', user=current_user, name=userName[0], s=session)

    # Retorna a página de configuração de usuário do tipo voluntário

    @staticmethod
    def getVolunteerConfigPage():
        if request.method == 'GET':
            return render_template('user/config.html')

        tipo = request.form.get('tipo')
        if current_user.user_type is '' or current_user.user_type is None:
            current_user.user_type = tipo
            db.session.add(current_user)

        if tipo == 'V':
            vol = Voluntario(current_user.id, '')
            db.session.add(vol)

        else:
            lar = Lar(current_user.id)
            db.session.add(lar)

        db.session.commit()
        return redirect('/')

    # retorna a página de visitas

    @staticmethod
    def getVisitHomePage():

        lares = db.session.query(Lar.id, Lar.nome).limit(8).all()

        if current_user.user_type._value_ == 'V':
            rs_visits = Visita.query.filter_by(id_usuario=current_user.id).limit(3).all()
        else:
            rs_lar = Lar.query.filter_by(id_usuario=current_user.id).first()
            rs_visits = Visita.query.filter_by(nome_lar=rs_lar.nome).limit(3).all()

        return render_template('visit/home.html',
                               lares=lares,
                               visitas=rs_visits)

    # Retorna a página para marcar visitas

    @staticmethod
    def getBookVisitPage(request_id):

        lar = Lar.query.filter_by(id=request_id).first()

        if request.method == "GET":
            return render_template('visit/book.html', lar=lar)

        id_usuario = current_user.id
        lar_id = lar.id
        volunteer_name = request.form.get('name')
        lar_name = lar.nome

        # Faz a formatação da data
        visit_date = request.form.get('visit-date')
        date = map(lambda item: int(item), visit_date.split('-'))
        date = list(date)
        fdate = datetime(date[0], date[1], date[2])
        visit_date = fdate.date()

        # Faz a formatação da hora
        visit_hour = request.form.get('visit-hour')
        visit_hour = map(lambda item: int(item), visit_hour.split(':'))
        visit_hour = list(visit_hour)
        fhour = datetime(1999, 1, 1, visit_hour[0], visit_hour[1])
        visit_hour = fhour.time()

        visit_reason = request.form.get('visit-reason')

        visit = Visita(id_usuario, lar_id, volunteer_name, lar_name,
                       visit_date, visit_hour, visit_reason)

        db.session.add(visit)
        db.session.commit()

        flash('Visita marcada com sucesso!', 'success')
        return redirect('/usuarios/visit')

    # Retorna o dashboard das visitas

    @staticmethod
    def getDashboard():
        if current_user.user_type._value_ == 'V':
            rs_visits = Visita.query.filter_by(id_usuario=current_user.id)
        else:
            rs_lar = Lar.query.filter_by(
                id_usuario=current_user.id).first()
            rs_visits = Visita.query.filter_by(nome_lar=rs_lar.nome)
        return render_template('visit/dashboard.html', visitas=rs_visits)

    # Deleta a visita do banco de dados

    @staticmethod
    def deleteVisitLink(id):
        visit = Visita.query.filter_by(id=id).first()
        db.session.delete(visit)
        db.session.commit()

        flash('Visita deletada com sucesso!', 'success')
        return redirect('/usuarios/dashboard')

    # GET: Retorna a página de edição da visita, POST: edita a visita

    @staticmethod
    def editVisitPage(id):
        visit = Visita.query.filter_by(id=id).first()
        if request.method == "GET":
            return render_template('visit/edit.html', visit=visit)

        # Faz a formatação da data
        visit_date = request.form.get('visit-date')
        date = map(lambda item: int(item), visit_date.split('-'))
        date = list(date)
        fdate = datetime(int(date[0]), int(date[1]), int(date[2]))
        visit_date = fdate.date()

        # Faz a formatação da hora
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
        lar = Lar.query.filter_by(id=id).first()
        return f'ID: {lar.id}<br> NOME: {lar.nome}<br> LINK: <a href="/usuarios/book/{lar.id}">Marcar visita</a>'

    @staticmethod
    def save_name():
        if current_user.user_type._value_ == 'L':
            user = Lar.query.filter_by(id_usuario=current_user.id).first()
            user.nome = request.form.get('nome')
        else:
            user = Voluntario.query.filter_by(id_usuario=current_user.id).first()
            user.nome = request.form.get('nome')

        db.session.add(user)
        db.session.commit()
        return redirect('/usuarios/profile')

    @staticmethod
    def get_all_lares_page():
        if current_user.user_type._value_ == 'L':
            user = Lar.query.filter_by(id_usuario=current_user.id).first()
        else:
            user = Voluntario.query.filter_by(id_usuario=current_user.id).first()

        return render_template('visit/all_lares_page.html', nome=user.nome)

    @staticmethod
    def get_lar_page():
        if current_user.user_type._value_ == 'L':
            user = Lar.query.filter_by(id_usuario=current_user.id).first()
        else:
            user = Voluntario.query.filter_by(id_usuario=current_user.id).first()
        return render_template('visit/lar.html', nome=user.nome)
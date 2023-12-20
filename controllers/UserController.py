from flask import render_template, redirect, flash, session, request
from models import Usuario, Voluntario, Visita, Lar, Notificacao
from utils import db
from flask_login import current_user, logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
import main
import uuid as uuid
import os


class User():

    # retorna a página de usuário
    @staticmethod
    def get_home():
        if "id_info" not in session:
            u_id = current_user.id
            if current_user.user_type._value_ == 'L':
                user = Lar.query.filter_by(id_usuario=u_id).first()
            else:
                user = Voluntario.query.filter_by(id_usuario=u_id).first()

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
            user = Lar.query.filter_by(id_usuario=u_id).first()
        else:
            user = Voluntario.query.filter_by(id_usuario=u_id).first()

        return render_template('user/profile.html', user=user, name=user.nome, s=session)

    # Retorna a página de configuração de usuário

    @staticmethod
    def get_config_page():
        if request.method == 'GET':
            return render_template('user/config.html')

        tipo = request.form.get('tipo')
        if current_user.user_type is '' or current_user.user_type is None:
            current_user.user_type = tipo
            db.session.add(current_user)

        if tipo == 'V':

            vol = Voluntario(current_user.id)
            if session['id_info']:
                vol.foto = session['id_info']['picture']
                vol.nome = session['id_info']['given_name']
            db.session.add(vol)

        else:
            lar = Lar(current_user.id)
            if session['id_info']:
                lar.foto = session['id_info']['picture']
                lar.nome = session['id_info']['given_name']
            db.session.add(lar)

        db.session.commit()
        return redirect('/')

    # retorna a página de visitas

    @staticmethod
    def get_visit_home_page():
        if current_user.user_type._value_ == 'V':
            user = Voluntario.query.filter_by(id_usuario=current_user.id).first()
            rs_visits_up = Visita.query.filter(Visita.id_voluntario == user.id, Visita.status != 'C').limit(3).all()
            rs_visits_down = Visita.query.filter(Visita.id_voluntario == user.id, Visita.status == 'C').limit(3).all()

            for visit in rs_visits_up:
                lar = Lar.query.filter_by(id=visit.id_lar).first()
                visit.nome = lar.nome

            for visit in rs_visits_down:
                lar = Lar.query.filter_by(id=visit.id_lar).first()
                visit.nome = lar.nome

        elif current_user.user_type._value_ == 'L':
            user = Lar.query.filter_by(id_usuario=current_user.id).first()
            rs_visits_up = Visita.query.filter(Visita.id_lar == user.id, Visita.status != 'C').limit(3).all()
            rs_visits_down = Visita.query.filter(Visita.id_lar == user.id, Visita.status == 'C').limit(3).all()
            for visit in rs_visits_up:
                voluntario = Voluntario.query.filter_by(id=visit.id_voluntario).first()
                visit.nome = voluntario.nome
            for visit in rs_visits_down:
                voluntario = Voluntario.query.filter_by(id=visit.id_voluntario).first()
                visit.nome = voluntario.nome

        return render_template('visit/home.html', visitas_down=rs_visits_down, visitas_up=rs_visits_up, user=user,)

    # Retorna a página para marcar visitas

    @staticmethod
    def get_book_visit_page(request_id):

        lar = Lar.query.filter_by(id=request_id).first()
        if lar.principais_necessidades == '':
            abort(404)

        if request.method == "GET":
            return render_template('visit/book.html', lar=lar)

        id_usuario = current_user.id
        vol = Voluntario.query.filter_by(id_usuario=id_usuario).first()
        lar_id = lar.id
        volunteer_name = request.form.get('name')
        visit_date = request.form.get('visit-date')
        qnt = request.form.get('qnt')
        visit_date = visit_date.split('T')
        v_datetime = '{} {}'.format(visit_date[0], visit_date[1])
        visit_reason = request.form.get('visit-reason')
        lar_name = lar.nome

        visit = Visita(vol.id, request_id, lar_name, v_datetime, visit_reason, 'P', qnt)
        notify = Notificacao(current_user.id, lar.id_usuario, f'{vol.nome} deseja fazer uma visita', True)

        db.session.add(visit)
        db.session.add(notify)
        db.session.commit()

        flash('Visita marcada com sucesso!', 'success')
        return redirect('/usuarios/visit')

    # Retorna o dashboard das visitas

    @staticmethod
    def get_dashboard_page():
        page = request.args.get('page', 1, type=int)
        if current_user.user_type._value_ == 'V':
            vol = Voluntario.query.filter_by(id_usuario=current_user.id).first()
            rs_visits = Visita.query.filter(Visita.id_voluntario==vol.id, Visita.status != 'C').paginate(page=page, per_page=3)

            for visit in rs_visits.items:
                lar_id = visit.id_lar
                lar = Lar.query.filter_by(id=lar_id).first()
                visit.nome = lar.nome
        else:
            rs_lar = Lar.query.filter_by(
                id_usuario=current_user.id).first()
            rs_visits = Visita.query.filter_by(id_lar=rs_lar.id)

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
        page = request.args.get('page', 1, type=int)
        lares = Lar.query.paginate(page=page, per_page=3)
        for lar in lares.items:
            user = Usuario.query.filter_by(id=lar.id).first()
            lar.email = user.email

        if current_user.user_type._value_ == 'L':
            user = Lar.query.filter_by(id_usuario=current_user.id).first()
        else:
            user = Voluntario.query.filter_by(id_usuario=current_user.id).first()

        return render_template('visit/all_lares_page.html', user=user, lares=lares)

    @staticmethod
    def get_lar_page(id):
        lar = Lar.query.filter_by(id=id).first()
        email = Usuario.query.filter_by(id=lar.id_usuario).first()
        if lar.principais_necessidades == '':
            abort(404)

        if current_user.user_type._value_ == 'L':
            user = Lar.query.filter_by(id_usuario=current_user.id).first()
        else:
            user = Voluntario.query.filter_by(id_usuario=current_user.id).first()
        return render_template('visit/lar.html', user=user, lar=lar, email=email.email)

    @staticmethod
    def save_data():
        if current_user.user_type._value_ == 'L':
            user = Lar.query.filter_by(id_usuario=current_user.id).first()
            user.principais_necessidades = request.form.get('principais')
            user.pix = request.form.get('pix')
            user.telefone = request.form.get('tel')
            user.cep = request.form.get('cep')
            user.instagram = request.form.get('insta')
        else:
            user = Voluntario.query.filter_by(id_usuario=current_user.id).first()
            user.telefone = request.form.get('tel')

        db.session.add(user)
        db.session.commit()

        return redirect('/usuarios/profile')

    @staticmethod
    def get_notification_page():
        if current_user.user_type._value_ == 'V':
            user = Voluntario.query.filter_by(id_usuario=current_user.id).first()
        else:
            user = Lar.query.filter_by(id_usuario=current_user.id).first()


        notificacoes = Notificacao.query.filter_by(id_destino=current_user.id).all()
        for notify in notificacoes:
            id = notify.id_remetente
            if current_user.user_type._value_ == 'V':
                user_query = Lar.query.filter_by(id_usuario=id).first()
                notify.foto = user_query.foto
            else:
                user_query = Voluntario.query.filter_by(id_usuario=id).first()
                notify.foto = user_query.foto

        return render_template('visit/notificacao.html', notificacoes=notificacoes, user=user)

    @staticmethod
    def get_volunteer_page(id):
        if current_user.user_type._value_ == 'V':
            redirect('/usuarios/')
        user = Lar.query.filter_by(id_usuario=current_user.id).first()
        vol = Voluntario.query.filter_by(id_usuario=id).first()
        return render_template('visit/volunteer.html', voluntario=vol, user=user)

    @staticmethod
    def deny_volunteer(id):
        vol = Voluntario.query.filter_by(id_usuario=id).first()
        lar = Lar.query.filter_by(id_usuario=current_user.id).first()
        visit = Visita.query.filter_by(id_voluntario=vol.id, id_lar=lar.id, status='P').first()
        if not visit:
            return redirect('/usuarios/notificacoes')

        visit.status = 'N'
        notfi = Notificacao.query.filter_by(id_remetente=id, id_destino=current_user.id).first()
        lar = Lar.query.filter_by(id_usuario=current_user.id).first()
        new_notfi = Notificacao(mensagem=f'Sua visita ao lar {lar.nome} foi negada', id_remetente=current_user.id,
                                id_destino=id, eacao=False)

        db.session.add(visit)
        db.session.add(new_notfi)
        db.session.delete(notfi)

        db.session.commit()
        return redirect('/usuarios/notificacoes')

    @staticmethod
    def accept_volunteer(id):
        vol = Voluntario.query.filter_by(id_usuario=id).first()
        lar = Lar.query.filter_by(id_usuario=current_user.id).first()
        visit = Visita.query.filter_by(id_voluntario=vol.id, id_lar=lar.id, status='P').first()
        if not visit:
            return redirect('/usuarios/notificacoes')

        visit.status = 'A'
        notfi = Notificacao.query.filter_by(id_remetente=id, id_destino=current_user.id).first()
        lar = Lar.query.filter_by(id_usuario=current_user.id).first()
        new_notfi = Notificacao(mensagem=f'{lar.nome.capitalize()} aceitou seu pedido de visita', id_remetente=current_user.id,
                                id_destino=id, eacao=False)

        db.session.add(visit)
        db.session.add(new_notfi)
        db.session.delete(notfi)

        db.session.commit()
        return redirect('/usuarios/notificacoes')

    @staticmethod
    def save_foto(id):
        foto = request.files.get('foto')
        pic_filename = secure_filename(foto.filename)
        pic_name = str(uuid.uuid1()) + '_' + pic_filename

        if current_user.user_type._value_ == 'V':
            user = Voluntario.query.filter_by(id_usuario=current_user.id).first()
        else:
            user = Lar.query.filter_by(id_usuario=current_user.id).first()

        foto.save(os.path.join(os.path.abspath(main.app.config['UPLOAD_FOLDER']), pic_name))
        user.foto = pic_name

        db.session.add(user)
        db.session.commit()
        return redirect('/usuarios/profile')

    @staticmethod
    def realize(id):
        visit = Visita.query.filter_by(id=id).first()
        visit.status = 'C'

        db.session.add(visit)
        db.session.commit()

        flash('Visita marcada como realizada com sucesso!', 'success')
        return redirect('/usuarios/dashboard')

    @staticmethod
    def get_realized_page():
        page = request.args.get('page', 1, type=int)
        if current_user.user_type._value_ == 'V':
            vol = Voluntario.query.filter_by(id_usuario=current_user.id).first()
            rs_visits = Visita.query.filter_by(id_voluntario=vol.id, status ='C').paginate(page=page,per_page=3)


            for visit in rs_visits.items:
                lar_id = visit.id_lar
                lar = Lar.query.filter_by(id=lar_id).first()
                visit.nome = lar.nome
        else:
            rs_lar = Lar.query.filter_by(
                id_usuario=current_user.id).first()
            rs_visits = Visita.query.filter_by(id_lar=rs_lar.id)

        return render_template('visit/dashboard_realizadas.html', visitas=rs_visits)
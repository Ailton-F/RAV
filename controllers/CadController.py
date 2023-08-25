from flask import render_template, request, redirect, flash, session, abort
from flask_login import login_user
from models import Usuario
from utils import db
from google.oauth2 import id_token
from pip._vendor import cachecontrol
from google_auth_oauthlib.flow import Flow
import os, pathlib, requests, json, google.auth.transport.requests, bcrypt

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client_secrets_file = os.path.join(pathlib.Path(), "client_secret.com.json")
secret_file = open(client_secrets_file)
secret_data = json.load(secret_file)
flow = Flow.from_client_secrets_file(
  client_secrets_file=client_secrets_file,
  scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
  redirect_uri="http://127.0.0.1:5000/cadastro/callback",
)
GOOGLE_CLIENT_ID = secret_data['web']['client_id']


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
        if senha != csenha:
          flash('Senhas diferentes', 'danger')
          return redirect('/cadastro')
        
        # Adding the salt to password
        salt = bcrypt.gensalt()
        # Hashing the password
        senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
        
        usuario = Usuario(email, senha, admin, user_type, 1)
        usuario_existe = Usuario.query.filter_by(email = email).first()

        if usuario_existe and usuario.email in usuario_existe.email:
          flash('Email já cadastrado', 'danger')
          return redirect('/cadastro')
          

        db.session.add(usuario)
        db.session.commit()
        
        login_user(usuario)
      except:
        flash('Erro interno, por favor aguarde', 'danger')
        return redirect('/cadastro')
      
      return redirect('/usuarios/user_config')
    
  @staticmethod
  def getGoogleCad():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

  @staticmethod
  def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!
    
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    usuario = Usuario(
      id_info.get('email'),
      None,
      False,
      None,
      1,
    )

    usuario_existe = Usuario.query.filter_by(email = usuario.email).first()
    if usuario_existe and usuario.email in usuario_existe.email:
      flash('Email já cadastrado', 'danger')
      return redirect('/login')

    db.session.add(usuario)
    db.session.commit()
    
    login_user(usuario)
    return redirect("/usuarios/user_config")
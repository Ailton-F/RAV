from flask import render_template, request, redirect, flash, session, abort
from models import Usuario
from flask_login import login_user
from google.oauth2 import id_token
from pip._vendor import cachecontrol
from google_auth_oauthlib.flow import Flow
import os, pathlib, requests, json, google.auth.transport.requests

client_secrets_file = os.path.join(pathlib.Path(), "client_secret.com.json")
secret_file = open(client_secrets_file)
secret_data = json.load(secret_file)
flow = Flow.from_client_secrets_file(
  client_secrets_file=client_secrets_file,
  scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
  redirect_uri="http://127.0.0.1:5000/login/callback",
)
GOOGLE_CLIENT_ID = secret_data['web']['client_id']
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
      
  @staticmethod
  def getGoogleLogin():
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

    session["google_id"] = id_info.get("sub")
    session["nome"] = id_info.get("name")
    return redirect("/usuarios")
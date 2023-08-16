import pathlib
import os
import routes
import json

from flask import Flask, render_template, redirect
from flask_migrate import Migrate
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from flask_login import current_user
from dotenv import load_dotenv
from utils import db, lm

load_dotenv()

file=open('client_secret.com.json')
data=json.load(file)

app = Flask(__name__)
app.secret_key = data['web']['client_secret']
GOOGLE_CLIENT_ID = data['web']['client_id']
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


for bluePrint in routes.__all__:
    app.register_blueprint(bluePrint, url_prefix=f'/{bluePrint.name}')

migrate = Migrate(app, db)
conexao = os.getenv("MYSQL_URI")
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.com.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost/callback"
)

db.init_app(app)
lm.init_app(app)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/usuarios/')
    return render_template('home.html')


# with app.app_context():
#   db.drop_all()
#   db.create_all()

app.run(debug=True)

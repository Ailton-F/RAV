from flask import Flask, render_template, redirect
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
from flask_login import current_user
from dotenv import load_dotenv
from utils import db, lm
import os
import routes

load_dotenv()

app = Flask(__name__)
app.secret_key = '094&U%!2Hdbf'
socket = SocketIO(app, cors_allowed_origins="*")

for bluePrint in routes.__all__:
    app.register_blueprint(bluePrint, url_prefix=f'/{bluePrint.name}')

migrate = Migrate(app, db)
conexao = os.getenv("MYSQL_URI")
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
lm.init_app(app)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/usuarios/')
    return render_template('home.html')


@socket.on('message')
def handle_message(data):
    data['email'] = current_user.email
    data['id'] = current_user.id
    print(data)
    emit('message', data, broadcast=True)


# with app.app_context():
#   db.drop_all()
#   db.create_all()

app.run(debug=True)

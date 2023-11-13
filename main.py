
import os, routes, json
from flask import Flask, render_template, redirect
from flask_migrate import Migrate
from flask_login import current_user
from dotenv import load_dotenv
from utils import db, lm

load_dotenv()
app = Flask(__name__)
app.secret_key = "X%&@BX"

for bluePrint in routes.__all__:
    app.register_blueprint(bluePrint, url_prefix=f'/{bluePrint.name}')

migrate = Migrate(app, db)
conexao = os.getenv("MYSQL_URI")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
lm.init_app(app)


@app.errorhandler(404)
def not_found(e): return render_template('errors/404.html', e=e)
@app.errorhandler(500)
def internal(e): return render_template('errors/500.html', e=e)
@app.errorhandler(403)
def forbidden(e): return render_template('errors/403.html', e=e)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/usuarios/')
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

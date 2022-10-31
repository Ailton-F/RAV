from flask import Flask, render_template
from database import db
import routes
from flask_migrate import Migrate
from models import Usuario
from models import Doacao

app = Flask(__name__)
app.secret_key =  'analin'
for bluePrint in routes.__all__:
  app.register_blueprint(bluePrint)

db.init_app(app)
migrate = Migrate(app, db)
conexao = "sqlite:///meubanco.db"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

@app.route('/')
def index():
    return render_template('home.html')

app.run(host='0.0.0.0', port=81)
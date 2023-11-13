from flask import Blueprint, session, abort
from utils import lm
from controllers import cad, user
from flask_login import login_required, current_user
from models import Usuario

users_bl = Blueprint("usuarios", __name__)

@lm.user_loader
def load_user(id): return Usuario.query.get(id)

@users_bl.route('/')
@login_required
def home(): return user.getHome()

@users_bl.route('/chat')
@login_required
def chatPage(): return user.getChatPage()

@users_bl.route('/profile', methods=['GET'])
@login_required
def profile_page(): return user.getProfilePage()

@users_bl.route('/admin', methods=['GET'])
@login_required
def admin_page(): return user.getAdminPage() 

@users_bl.route('/logoff', methods=['POST'])
@login_required
def logoff(): return user.logUserOff()

@users_bl.route('/chat_template')
@login_required
def msgTemplate(): return user.getMsgTemplate()
  
@users_bl.route('/create', methods=['GET', 'POST'])
def insert(): return cad.create()
  
@users_bl.route('/delete/<int:id>/', methods=['POST'])
@login_required
def delete(id): return user.deleteUser(id)

@users_bl.route('/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id): return user.editUser(id)

@users_bl.route('/user_config', methods=['GET', 'POST'])
@login_required
def volunteerConfigPage(): return user.getVolunteerConfigPage()
@users_bl.route('/visit', methods=["GET"])
@login_required

def visitHomePage(): return user.getVisitHomePage()

@users_bl.route('/visit/<int:id>', methods=['GET'])
@login_required

def asylumProfile(id): return user.getAsylumProfile(id)

@users_bl.route('/book/<int:id>', methods=["GET", "POST"])
@login_required

def bookVisit(id): return user.getBookVisitPage(id)

@users_bl.route('/dashboard', methods=["GET", "POST"])
@login_required

def dashboard(): return user.getDashboard()

@users_bl.route('/delete_visit/<int:id>', methods=["POST"])
@login_required
def deleteVisit(id): return user.deleteVisitLink(id)

@users_bl.route('/edit_visit/<int:id>', methods=["GET", "POST"])
@login_required
def editVisit(id): return user.editVisitPage(id)
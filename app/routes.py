from flask import redirect, render_template,\
    url_for, flash, request
from flask_login import login_required, current_user,\
    login_user
from werkzeug.urls import url_parse

from app import application as main
from app import login
from .database import User, Doctor, Patient,\
    Pregnant, Child


@main.route('/', methods=['POST', 'GET'])
def sing_in():  
    return render_template("main/sign_in.html")


@main.route('/panel', methods=['POST', 'GET'])
@login_required
def panel():
    return 'panel'


@login.user_loader
@login_required
def load_user(id):
    return User.query.get(int(id))
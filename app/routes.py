from flask import redirect, render_template,\
    url_for, flash, request
from flask_login import login_required, current_user,\
    login_user

from app import application as main
from app import login
from .database import User, Doctor, Patient,\
    Pregnant, Child


@main.route('/', methods=['POST', 'GET'])
def sing_in():  
    if current_user.is_authenticated:
        return redirect(url_for('panel'))

    if request.method == 'POST':
        login = "login"
        password = "password"
        user = User.query.filter_by(login=login).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('sing_in'))
        login_user(user)
        return redirect(url_for('panel'))
            
    return render_template('main/panel.html')


@main.route('/panel', methods=['POST', 'GET'])
def panel():
    return 'panel'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
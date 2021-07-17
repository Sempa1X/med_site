from flask import Blueprint, render_template, redirect,\
    url_for, request, flash

from app import db
from app.src.database import User

from flask_login import current_user, login_user,\
    login_required, logout_user


bp_login = Blueprint('login', __name__, url_prefix='/')


@bp_login.route('/', methods=['POST', 'GET'])

def login():
    if request.method == 'POST':
        print(request.form.get('username'), request.form.get('password'))
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user is None or not user.check_password(request.form.get('password')):
            flash('Пароль или имя пользователя не верны!')
            return redirect(url_for('login.login'))
        login_user(user)
        return redirect(url_for('receptions.reception'))

    return render_template('login/login.html')


@bp_login.route('/logout')

def logout():
    logout_user() 
    return redirect(url_for('login.login'))


from flask import redirect, render_template,\
    url_for, flash, request
from flask_login import login_required, current_user,\
    login_user
from werkzeug.urls import url_parse

from app import application
from app import login
from .database import User


@application.route('/', methods=['POST', 'GET'])
def sing_in():  
<<<<<<< HEAD
    if current_user.is_authenticated:
        return redirect(url_for('panel'))

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(login=login).first()
        
        if user.passwd == password:
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('panel')
            return redirect(next_page)      
        else:    
            flash('Invalid username or password')
            return redirect(url_for('sing_in'))

    return render_template('sing_in.html')


@application.route('/panel', methods=['POST', 'GET'])
=======
    return render_template("main/sign_in.html")


@main.route('/panel', methods=['POST', 'GET'])
>>>>>>> 06fc7776d89d77ba25a4f719106c86992043e0dc
@login_required
def panel():
    return 'panel'


@login.user_loader
@login_required
def load_user(id):
    return User.query.get(int(id))
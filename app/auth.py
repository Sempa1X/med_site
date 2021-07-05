from flask import redirect, render_template,\
    url_for, flash, request, Blueprint
from flask_login import login_required, current_user,\
    login_user, logout_user
from werkzeug.urls import url_parse

from app import login
from .database import User


bp_auth = Blueprint('auth', __name__, template_folder='templates/test') 


# @bp_auth.route('/')
# def sign_in():  
    

    


@bp_auth.route('/', methods=['GET', 'POST'])
def sign_in():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.panel'))

    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(login=login).first()
        
        if user is None or user.passwd != password:
            print(f'\n\n\n\n\n\n{user.passwd} {password}  {login}\n\n\n\n\n\n')
            flash('Invalid username or password')
            return redirect(url_for('auth.sign_in')) 
        else:   
            print(f'\n\n\n\n\n\n{user.passwd} {password}\n\n\n\n\n\n')
            login_user(user)
            # next_page = request.args.get('next')
            # if not next_page or url_parse(next_page).netloc != '':
            #     next_page = url_for('main.panel')
            return redirect(url_for('main.panel')) 
    
    return render_template('sign_in.html')


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.panel'))


@login.user_loader
@login_required
def load_user(id):
    return User.query.get(int(id))


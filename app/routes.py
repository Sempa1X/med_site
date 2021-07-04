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
    # if current_user.is_authenticated:
    #     return redirect(url_for('panel'))

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        # user = User.query.filter_by(login=login).first()
        # doc = Doctor.query.filter_by(login=login).first()
        
        # if not user.check_password(password):
        #     #login_user(user)
        #     return redirect(url_for('panel'))

        # elif not doc.check_password(password):
        #     #login_user(doc)
        #     return redirect(url_for('panel'))
        
        # # else:    
        # #     flash('Invalid username or password')
        # #     return redirect(url_for('sing_in'))
        

        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page)      
    return render_template('sing_in.html')


@main.route('/panel', methods=['POST', 'GET'])
#@login_required
def panel():
    return 'panel'


@login.user_loader
@login_required
def load_user(id):
    return User.query.get(int(id))
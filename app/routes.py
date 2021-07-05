"""
Файл для логики путей сайта
"""
# импортируем стандартные модули
from datetime import datetime
import os

# импортируем установленные модули
from flask import redirect, url_for,\
    render_template, flash, request, g
from flask_login import current_user, login_required, \
    login_user, logout_user
from sqlalchemy import or_, and_

# импортируем свои файлы
from app import application, db, login
from app.models import User, Record

# переменные 

# получение количества товара в корзине
# каждого пользователя и испоьзуем в base.html
@application.before_request
def before_request():
    pass
    # if current_user.is_authenticated:
    #     return redirect(url_for('login'))    


@application.route('/todo', methods=['GET', 'POST'])
def todo():
    print(current_user.role)
    return render_template('todo.html')

# обработка станицы авторизации 
@application.route('/', methods=['GET', 'POST'])
def login():
    # если пользователя авторизован, перенаправить на главную
    if current_user.is_authenticated:
        return redirect(url_for('todo'))
    # если на отправили форму
    if request.method == 'POST':
        # получаем пользователя
        user = User.query.filter_by(username=request.form.get('username')).first()
        # Если username или пароль не верны, то вывести сообщение и обновить страницу
        if user is None or not user.check_password(request.form.get('password')):
            flash('Пароль или имя пользователя не верны!')
            return redirect(url_for('login'))
        # авторизуем пользователя и перенаправляем на главную
        login_user(user)
        return redirect(url_for('todo'))
    return render_template('main/login.html', title='Золотые ручки - Авторизация')


# обработка станицы регистрации
@application.route('/register_staff', methods=['GET', 'POST'])
def register():
    # ксли пользователь авторизован перенаправляем на главню
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    # если отправили форму
    if request.method == 'POST':
        # добавляем пользователя и отправляем сообщение и перенаправляем на авторизацию
        user = User(username=request.form.get('username'), email=request.form.get('email'))
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрирваны!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Золотые ручки - Регистрация')


# обработка станицы деавторизации
@application.route('/logout')
@login_required
def logout():
    logout_user() # деавторизация и переходим на авторизацию
    return redirect(url_for('login'))



@application.errorhandler(404)
@login_required
def error_404(error):
    return render_template("main/404.html", error=error, user_role="doctor")



@application.route("/panel", methods=['GET', 'POST'])
@login_required
def panel():
    return render_template("main/panel.html",)


@application.route("/record", methods=['GET', 'POST'])
@login_required
def record():
    return render_template("main/doctor_record.html")



@application.route("/reception", methods=['GET', 'POST'])
@login_required
def reception():
    reasons = Record.query.all()
    if request.method == 'POST':
        calendar = request.form.get('calendar')
        radio_false = request.form.get('radio_false')
        radio_true = request.form.get('radio_true')

        if radio_false == None and radio_true == None:
            flash('Вы не выбрали пришел пациент или нет!')    
        
        print(calendar, radio_false, radio_true)

    return render_template("main/doctor_reception.html", receptions=reasons)






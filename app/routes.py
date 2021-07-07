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



@application.route("/record", methods=['GET', 'POST'])
@login_required
def record():
    return render_template("main/doctor_record.html")



@application.route("/reception", methods=['GET', 'POST'])
@login_required
def reception():
    reasons = Record.query.all()
    doctors = User.query.filter(and_(User.isActive=='True', User.role=="doctor"))
    doc_id = []

    for i in doctors:
        doc_id.append(i.id)
    
    if request.method == 'POST' and "btn-select" in request.form:

    #datetime.now().strftime('%d.%m.%Y'))
    #datetime.now().strftime('%H:%M'))
        calendar = request.form.get('calendar')
        select_doc = request.form.get('select_doc')
        access_date = []
        global access_recept
        global access_recept2

        for i in doc_id:
            if select_doc == 'doctor_all':
                receptions = Record.query.all()
                for i in receptions:
                    date_split = str(i.date)
                    if date_split.split(' ')[0] == calendar:
                        access_date.append(i.id)
                for i in access_date:
                    access_recept = Record.query.filter_by(id = i)
                return render_template("main/doctor_reception.html", receptions=access_recept, doctors=doctors)

            elif select_doc == f'doctor_{i}':
                doctor = User.query.get(i)
                receptions = Record.query.filter_by(doctor_id = i)
                for i in receptions:
                    date_split = str(i.date)
                    if date_split.split(' ')[0] == calendar:
                        access_date.append(i.id)
                for i in access_date:
                    access_recept2 = Record.query.filter_by(id = i)
                return render_template("main/doctor_reception.html", receptions=access_recept2, doctor=doctor, doctors=doctors)

    if request.method == 'POST' and "btn-close" in request.form:
        radio = request.form.get('radioBTN')
           
        if radio == None:
            flash('Не выбрано действие', "primary")
        elif radio == "option1":
            flash('Пациент пришел', "success")
        elif radio == "option2":
            flash('Пациент не пришел', "primary") 
        


    return render_template("main/doctor_reception.html", receptions=reasons, doctors=doctors)


@application.route("/reception_post", methods=['POST'])
@login_required
def reception_post():
    doctors = User.query.filter(and_(User.isActive=='True', User.role=="doctor"))
    


# обработка станицы авторизации 
@application.route('/', methods=['GET', 'POST'])
def login():
    # если пользователя авторизован, перенаправить на главную
    if current_user.is_authenticated:
        return redirect(url_for('reception'))
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
        return redirect(url_for('reception'))
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
    return render_template("main/404.html", error=error)








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
from app.models import User

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
    reasons = []
    reasons_get = [
        {
            'doctor': 'Абубакаров Абубакар Абубакович ',
            'pacient': 'Ебалай Александр Негрович',
            'time': datetime.now().strftime('%Y.%m.%d %H:%M'),
            'trust':'Четкий чел',
            'isActive': True,
            'reason': 'Хуй в глаз попал',
        },
        {
            'doctor': 'Зубенко Михаил Петрович ',
            'pacient': 'Ебалай Александр Негрович',
            'time':datetime.now().strftime('%Y.%m.%d %H:%M'), #'12.12.2012 12:12',
            'trust':'Не четкий чел',
            'isActive': True,
            'reason': 'Хуй в глаз попал',
        }, 
        {
            'doctor': 'Мамонт Ебучий Далдалушелович ',
            'pacient': 'Ебалай Александр Негрович',
            'time': datetime.now().strftime('%Y.%m.%d %H:%M'),
            'trust':'Четкий чел',
            'isActive': False,
            'reason': 'Хуй в глаз попал',
        }
    ]

    for i in reasons_get:
        time = str(i['time'])
        if i['isActive'] and time.split(' ')[0] ==  datetime.now().strftime('%Y.%m.%d'):
            print(time, time[0], time[1])
            i['time'] = time.split(' ')[1] 
            reasons.append(i)

    

    return render_template('todo.html', reasons=reasons)

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
def error_404(error):
    return render_template("main/404.html", error=error)



@application.route("/panel", methods=['GET', 'POST'])
@login_required
def panel():
    return render_template("main/panel.html", user_role='doctor')


@application.route("/record", methods=['GET', 'POST'])
@login_required
def record():
    return render_template("main/doctor_record.html", user_role='doctor')



@application.route("/reception", methods=['GET', 'POST'])
@login_required
def reception():
    aa = [["Трунов Д.И.", "18:00", 0, "Многие думают, что Lorem Ipsum - взятый с потолка псевдо-латинский набор слов, но это не совсем так. Его корни уходят в один фрагмент классической латыни 45 года н.э., то есть более двух тысячелетий назад. Ричард МакКлинток, профессор латыни из колледжа Hampden-Sydney, штат Вирджиния, взял одно из самых странных слов в Lorem Ipsum, 'consectetur', и занялся его поисками в классической латинской литературе. В результате он нашёл неоспоримый первоисточник Lorem Ipsum в разделах 1.10.32 и 1.10.33 книги 'de Finibus Bonorum et Malorum' ('О пределах добра и зла'), написанной Цицероном в 45 году н.э. Этот трактат по теории этики был очень популярен в эпоху Возрождения. Первая строка Lorem Ipsum,, происходит от одной из строк в разделе 1.10.32"], ["Азанов И.Е.", "19:00", 1, "Пизда заместо члена"]]
    return render_template("main/doctor_reception.html", user_role='doctor', receptions=aa)






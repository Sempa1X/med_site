"""
Файл для логики путей сайта
"""
# импортируем стандартные модули
import os

# импортируем установленные модули
from flask import redirect, url_for,\
    render_template, flash, request, g
from flask_login import current_user, login_required, \
    login_user, logout_user
from sqlalchemy import or_, and_

# импортируем свои файлы
from app import application, db, login
from app.models import User, Production, Backet

# переменные 
url = application.config['UPLOAD_FOLDER']

# получение количества товара в корзине
# каждого пользователя и испоьзуем в base.html
@application.before_request
def before_request():
    # если пользователь авторизован
    if current_user.is_authenticated:
        # получаем его товары
        back = Backet.query.filter_by(uid=current_user.id)
        counter = 0 # делаем счетчик
        for i in back: # для i в товарах прибавлять значение счетчика
            counter += 1
        g.backet_item_count = counter # заносим в переменню количество товаров


# обработка оплаты
@application.route('/buy/<price>')
@login_required # только авторизованные пользователи могут зайти на страницу
def buy(price):
    from cloudipsp import Api, Checkout
    api = Api(merchant_id=1396424, # создаем объект класса Api c параметрами
            secret_key='test')
    checkout = Checkout(api=api)# создаем объект класса Api c параметрами
    data = {
        "currency": "RUB",
        "amount": str(price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url) # перенаправляем на оплату


@application.route('/info/<id>')
def info(id):
    prod = Production.query.get(id) # получаем продукт по его ID
    prod.views += 1 # добавляем просмотр
    db.session.commit() # обновляем в базе значения
    return render_template('prod_info.html', prod=prod, title=f'Золотые руки - {prod.name}')


# обработка станицы /index и /
@application.route('/')
@application.route('/index')
def index():
    q = request.args.get('q')
    # Если поиск товара
    if request.args.get('q'):
        # получаем товары с названием запроса
        prod = Production.query.filter(Production.name.contains(q))
    else:
        # получаем все товары
        prod = Production.query.filter_by().all()
    return render_template('index.html', prods=prod, title='Золотые руки - Главная')


# обработка станицы добавления товара с обработкой пост и гет запросов
@application.route('/add_prod', methods=['GET', 'POST'])
def add_prod():
    if request.method == "POST":
        # получение значения с формы html
        prod_name = request.form.get('prod_name')
        prod_count = request.form.get('prod_count')
        prod_desc = request.form.get('prod_desc')
        prod_price = request.form.get('prod_price')
        # если есть фото
        if request.files['photo']:
            # проходим циклом по фоткам 
            i = request.files['photo']
            # сохраняем фотку на пк
            i.save(os.path.join(url, i.filename))
            photo = i.filename
            # добавляесм в базу
            prod = Production(name=prod_name, desc=prod_desc, count=prod_count, price=prod_price, photo=photo)
            db.session.add(prod)
            db.session.commit()
            # Выводим сообщение что товар добавлен
            flash('Продукт добавлен!')
            # перезагружаем страницу
            return redirect(url_for('index'))
        else:
            # иначе выводим что не все поля заполнены и обговляем страницу
            flash('Продукт не добавлен! не все поля заполнены')
            return redirect(url_for('index'))
    else:
        return render_template('add_prod.html', title='Золотые руки - Добавление товара')

    # загружаем страницу с параметрами для шаблонизатора
    return render_template('add_prod.html', title='Золотые руки - Добавление товара')


# обработка станицы о нас
@application.route('/about')
def about():
    # показ страницы 
    return render_template('about.html', title='Золотые ручки - О нас')


# обработка станицы пользователя
@application.route('/profile/<username>')
def profile(username):
    # получаем пользователя
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user, title='Золотые ручки - Профиль ' + current_user.username)


# обработка станицы авторизации 
@application.route('/auth', methods=['GET', 'POST'])
def login():
    # если пользователя авторизован, перенаправить на главную
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        return redirect(url_for('index'))
    return render_template('login.html', title='Золотые ручки - Авторизация')


# обработка станицы регистрации
@application.route('/register', methods=['GET', 'POST'])
def register():
    # ксли пользователь авторизован перенаправляем на главню
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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


# обработка станицы корзина
@application.route('/backeted/')
@login_required
def backeted():
    prc = []
    itms = []
    items = Backet.query.filter_by(uid=current_user.id)
    total = 0

    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    for i in items:
        if not None: # если товар не пустой 
            prods = Production.query.get(i.pid) # получаем товары из корзины
            itms.append(prods)    # добавляем в массив товары
            prc.append(prods.price) # добавляем в массив цену товаров      
    count = len(itms) # получаем кол-во товаров
    for am in prc:
        total += int(am) # получаем общую стоимость 
    
    return render_template('backet.html', title='Золотые ручки - Корзина', items=itms, count=count,total=str(total)) 


# обработка станицы добавления в корзину
@application.route('/add_backet/<pid>')
@login_required
def addBacket(pid):
    # если товар у пользователя есть то вывод сообщения
    if db.session.query(Backet).filter(or_((Backet.uid==current_user.id) & (Backet.pid == pid))).all():
        flash("Не возможно добавить товар, товар уже добавлен")
        return redirect(url_for('index'))
    # иначе добавляем товар и выводим сообщение
    else:
        backet = Backet(uid=current_user.id, pid=pid)
        db.session.add(backet)
        db.session.commit()   
        flash("Товар добавлен в корзину!")     
    return redirect(url_for('index'))




# обработка станицы удаления из корзины
@application.route('/del/<pid>')
@login_required
def del_backet(pid):
    # удаляем и переносим в корзину
    db.session.query(Backet).filter(and_((Backet.uid==current_user.id) & (Backet.pid == pid))).delete()
    db.session.commit()
    return redirect(url_for('backeted'))


# обработка станицы деавторизации
@application.route('/logout')
@login_required
def logout():
    logout_user() # деавторизация и переходим на авторизацию
    return redirect(url_for('login'))










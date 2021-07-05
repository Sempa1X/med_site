# подключаем встроенные библиотеки
from hashlib import md5

# подключаем установленные библиотеки
from sqlalchemy.dialects.sqlite import BLOB
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for

# подключаем свои файлы
from app import db, login

# создаем таблицу продукт
class Production(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(255))
    count = db.Column(db.Integer)
    price = db.Column(db.Integer)
    photo = db.Column(db.String(255))
    views = db.Column(db.Integer, default=0)
    buy_count = db.Column(db.Integer, default=0)
    

# создаем таблицу пользователь
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    isAdmin = db.Column(db.Boolean, default=False, nullable=False)
    
    # метод для установки пароля пользователю
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # метод для проверки пароля пользователя
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # метод для получения аватара
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

# создаем таблицу корзина
class Backet(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True) 
    uid = db.Column(db.Integer)
    pid = db.Column(db.Integer)


    # метод для проверки
    def check_backet(self, uid, pid):
        if uid == self.uid and pid == self.pid:
            return False
        else:
            return True


# создаем класс для настройки админ панели
class MyAdminView(ModelView):
    def is_accessible(self):
        return current_user.isAdmin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


# создаем класс для настройки лавной страницы админ панели
class MyIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.isAdmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        
    def is_visible(self):
    # This view won't appear in the menu structure
        return False



# добавляем пользователя в сессию
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


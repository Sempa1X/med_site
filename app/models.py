# подключаем встроенные библиотеки
from hashlib import md5
from datetime import datetime
from sqlalchemy.orm import backref

# подключаем установленные библиотеки
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for

# подключаем свои файлы
from app import db, login


# создаем таблицу пользователь
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    isAdmin = db.Column(db.Boolean, default=False, nullable=False)

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))

    sex = db.Column(db.Boolean, default=1)
    birthday = db.Column(db.String(50))
    
    phone = db.Column(db.String(50))
    phone2 = db.Column(db.String(50))
    email = db.Column(db.String(50))
    
    reg_time = db.Column(db.String(255), index=True, default=datetime.utcnow())
    isActive = db.Column(db.Boolean, default=True) # Работаспособность
    isAdmin = db.Column(db.Boolean, default=0)
    isDev =  db.Column(db.Boolean, default=0)
    division = db.Column(db.String(255))
    certificate = db.Column(db.String(255))
    role = db.Column(db.String(255), default='doctor')
    
    coment = db.Column(db.String(255))
    
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


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))

    birthday = db.Column(db.String(50))
    estimated_birthday = db.Column(db.String(255))
    num_fetus = db.Column(db.Integer)

    refer = db.Column(db.String(255))
    reception = db.Column(db.Boolean, default=True)
    
    lr_f_name = db.Column(db.String(255))
    lr_l_name = db.Column(db.String(255))
    lr_surname = db.Column(db.String(255))
    lr_status = db.Column(db.String(255))

    lr_pass_serial = db.Column(db.String(255))
    lr_pass_num = db.Column(db.String(255))
    lr_pass_date = db.Column(db.String(255))
    lr_pass_issued = db.Column(db.String(255))
    
    address = db.Column(db.String(255))
    trust_factor = db.Column(db.Boolean, default=True)
    pacient_role = db.Column(db.String(255))


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)

    doctor = db.Column(db.String(255))
    doctor_id = db.Column(db.Integer)
    patient_id = db.Column(db.Integer)
    pacient = db.Column(db.String(255))
    date = db.Column(db.String(255), index=True)
    time = db.Column(db.String(255), index=True)
    trust = db.Column(db.Boolean, default=True)
    isActive = db.Column(db.Boolean, default=True)
    reason = db.Column(db.String(255))



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


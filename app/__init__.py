from flask import Flask, url_for, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.menu import MenuLink

from config import Config


# Инициализация приложения Flask
application = Flask(__name__)
application.config.from_object(Config)

# Инициализация пользователей и авторизация и регистрация
login = LoginManager(application)
login.login_view = 'login.login'
login.login_message = "Доступ закрыт, войдите!"

# Инициализация базы данных
db = SQLAlchemy(application)
migrate = Migrate(application, db)

# BP
from app.blocks.login import bp_login
application.register_blueprint(bp_login)

from app.blocks.reception import bp_reception
application.register_blueprint(bp_reception)

from app.blocks.search import bp_search
application.register_blueprint(bp_search)

from app.blocks.add_patient import bp_add
application.register_blueprint(bp_add)

from app.blocks.list_expectation import bp_list_expectation
application.register_blueprint(bp_list_expectation)

from app.blocks.errors import bp_error
application.register_blueprint(bp_error)




from app.src.admin import MyIndexView, MyAdminView
from app.src.database import Record, User, Patient

admin = Admin(application, name='Medic', url='/admin', template_mode='bootstrap4', index_view=MyIndexView(name='Добавление персонала'))
admin.add_view(MyAdminView(Patient, db.session, name="Пациенты"))
admin.add_view(MyAdminView(Record, db.session, name="Записи"))
admin.add_view(MyAdminView(User, db.session, name="Персонал"))
admin.add_link(MenuLink(name='Назад', url='/'))

"""
Файл с помощью которого 
Python понимает что это пакет python
а не обычная дириктория
"""
# импортируем установленные модули
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_admin import Admin
from flask_admin.menu import MenuLink

# Устанавливаем значимые переменные которые
# будут использоватся во всем проекте
application = Flask(__name__, template_folder='html', static_folder='src')
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
login = LoginManager(application)
login.login_view = "login"
login.login_message = "Чтобы попасть на закрытые страницы, сначала авторизируйтесь!"

# Работа с админкой
from app.models import MyAdminView, MyIndexView,\
    Production, User, Backet

admin = Admin(application, name='Золотые руки', template_mode='bootstrap4', url='/', index_view=MyIndexView())
admin.add_view(MyAdminView(Production, db.session, name="Товары"))
admin.add_view(MyAdminView(Backet, db.session, name="Корзина"))
admin.add_view(MyAdminView(User, db.session, name="Пользователи"))
admin.add_link(MenuLink(name='Назад', url='/'))


# Делаем модули доступными для других файлов
from app import routes, models
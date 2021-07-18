from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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


# from app.src.database import MyIndexView


# admin = Admin(application, name='Shop', template_mode='bootstrap4', index_view=MyIndexView())
# admin.add_view(ModelView(Category, db.session, name="Категории"))
# admin.add_view(ModelView(Product, db.session, name="Товары"))

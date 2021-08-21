from threading import Lock

from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_mail import Mail

from config import Config


# Инициализация приложения Flask
application = Flask(__name__)
application.config.from_object(Config)


# Инициализация базы данных
metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)
db = SQLAlchemy(application, metadata=metadata)
migrate = Migrate(application, db, render_as_batch=True)
db.create_all() 

# Инициализация пользователей и авторизация и регистрация
login = LoginManager(application)
login.login_view = 'login.login'
login.login_message = "Доступ закрыт, войдите!"


# Инициализация и настройка почты
mail = Mail(application)
with application.app_context():
    from app.src.email import send_emails
    send_emails()



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

from app.blocks.office import bp_office
application.register_blueprint(bp_office)

from app.blocks.interview import bp_inter
application.register_blueprint(bp_inter)

bp_login._before_request_lock = Lock()
bp_reception._before_request_lock = Lock()
bp_search._before_request_lock = Lock()
bp_add._before_request_lock = Lock()
bp_list_expectation._before_request_lock = Lock()
bp_error._before_request_lock = Lock()
bp_office._before_request_lock = Lock()
bp_inter._before_request_lock = Lock()

bp_login._got_first_request = False
bp_reception._got_first_request = False
bp_search._got_first_request = False
bp_add._got_first_request = False
bp_list_expectation._got_first_request = False
bp_error._got_first_request = False
bp_office._got_first_request = False
bp_inter._got_first_request = False



from app.src.admin import MyIndexView, MyAdminView
from app.src.database import Record, User, Patient

admin = Admin(application, name='Medic', url='/admin', template_mode='bootstrap4', index_view=MyIndexView(name='Добавление персонала'))
admin.add_view(MyAdminView(Patient, db.session, name="Пациенты"))
admin.add_view(MyAdminView(Record, db.session, name="Записи"))
admin.add_view(MyAdminView(User, db.session, name="Персонал"))
admin.add_link(MenuLink(name='Назад', url='/'))

from app import blocks, src 

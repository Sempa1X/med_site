# import modules
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


# init application
application = Flask(__name__, template_folder='template')
application.config.from_object(Config)

# init database
db = SQLAlchemy(application)
migrate = Migrate(application, db)

# init and setting auth
# auth = LoginManager(application)
# auth.login_view('login.login')
# auth.login_message = "Авторизуйтесь, перед просмотром страницы!"


from app import database, routes
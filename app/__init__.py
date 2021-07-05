# import modules
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config



# init application
application = Flask(__name__, template_folder='templates')
application.config.from_object(Config)

# init database
db = SQLAlchemy(application)
migrate = Migrate(application, db)

# init and setting auth
login = LoginManager(application)
login.login_view = 'auth.sign_in'
login.login_message = "Авторизуйтесь, перед просмотром страницы!"

# init bp auth
from app.auth import bp_auth
application.register_blueprint(bp_auth, url_prefix='/')


# init bp main
from app.main import bp_main
application.register_blueprint(bp_main, url_prefix='/main')


from app import database, auth, main
import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Default settings
    FLASK_APP = 'run.py'
    DEBUG = True
    SECRET_KEY = "Secrets"
    USE_RELOADER=False

    # DataBase settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'medic.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Email sending settings
    IS_SENDER = False

    # GMAIL settings
    MAIL_USERNAME = 'iazanov471@gmail.com'
    MAIL_PASS = 'asdasdss228'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True

    # YANDEX settings
    Y_MAIL_USERNAME = 'Sempa1X@yandex.ru'
    Y_MAIL_PASS = 'asdasdss228'
    Y_MAIL_SERVER = 'smtp.yandex.ru'
    Y_MAIL_PORT = 465
    Y_MAIL_USE_SSL = True

    # Search
    ELASTICSEARCH_URL = \
        os.environ.get('ELASTICSEARCH_URL') # Устанавливаем значение для поиска
    

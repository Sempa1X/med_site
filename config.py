import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Default settings
    FLASK_APP = 'run.py'
    DEBUG = True
    SECRET_KEY = "Secrets"

    # DataBase settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'medic.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Настройка почты
    YANDEX_MAIL = 'sempa1x@yandex.ru'
    YANDEX_PASS = 'asdasdss228'

    # Search
    ELASTICSEARCH_URL = \
        os.environ.get('ELASTICSEARCH_URL') # Устанавливаем значение для поиска
    

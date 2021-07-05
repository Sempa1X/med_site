import os # импорт библиотеки os

# Записываем в переменную путь до файла
basedir = os.path.abspath(os.path.dirname(__file__)) 

# создаем класс Конфиг который наследует объект
class Config(object):
    # Default settings
    FLASK_APP = 'run.py' # устанавлеваем запускной файл
    DEBUG = True # Показывает ошибки
    SECRET_KEY = "Secrets" # устанавливаем секретный ключ
    
    # DataBase settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +\
        os.path.join(basedir, 'medic.db') # Устанавливаем где создается база данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # search
    ELASTICSEARCH_URL = \
        os.environ.get('ELASTICSEARCH_URL') # Устанавливаем значение для поиска
    


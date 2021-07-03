import os


base_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/")


class Config(object):
    # Default settings
    FLASK_APP = 'run.py' 
    DEBUG = True 
    SECRET_KEY = "Secrets" 
    #UPLOAD_FOLDER = base_dir + '\\app\\src\\img\\downloads'

    # DataBase settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +\
        os.path.join(base_dir, 'medic.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


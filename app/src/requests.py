from app import application, db, login, executor

@application.before_app_first_request
def before_request():
    pass

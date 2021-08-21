from app import application, db, login
from app.src.email import send_emails

@application.before_app_request
def before_request():
    send_emails()





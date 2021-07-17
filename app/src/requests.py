from app import application, db, login

@application.before_request
def before_request():
    pass
    # if current_user.is_authenticated:
    #     return redirect(url_for('login'))    

from flask import redirect, render_template,\
    url_for, flash, request, Blueprint
from flask_login import login_required, current_user,\
    login_user, logout_user
from werkzeug.urls import url_parse


bp_main = Blueprint('main', __name__) 


@bp_main.route('/')
@login_required
def panel():
    return 'panel'
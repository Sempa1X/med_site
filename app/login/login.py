from flask import Blueprint, render_template


bp_login = Blueprint('login', __name__)


@bp_login.route('/')
def login():
    return render_template('login\login.html')
from flask import Blueprint, render_template, redirect,\
    url_for, request, flash

from app import db
from app.src.database import User

from flask_login import current_user, login_user,\
    login_required, logout_user


bp_add = Blueprint('add', __name__, url_prefix='/add_patient')


@bp_add.route('/', methods=['POST', 'GET'])
@login_required
def add_patient():
    return render_template('add_patient/add_patient.html')

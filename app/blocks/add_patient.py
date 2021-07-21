from flask import Blueprint, render_template, redirect,\
    url_for, request, flash
from sqlalchemy import or_
from flask_login import current_user, login_user,\
    login_required, logout_user

from app import db
from app.src.database import Patient


bp_add = Blueprint('add', __name__, url_prefix='/add_patient')


@bp_add.route('/', methods=['GET'])
@login_required
def add_patient():
    return render_template('add_patient/add_patient.html')


@bp_add.route('/added', methods=['POST'])
def added():
    if 'data' in request.form or 'data' in request.args:
        print(request.form['data'])
        print(request.form['data']['surname'])
        return 'True'
    return 'false'




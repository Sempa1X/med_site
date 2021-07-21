from flask import Blueprint, render_template, redirect,\
    url_for, request, flash, jsonify
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
    data_replace = []
    for i in request.form:
        data_replace.append([i, request.form[i]])
    patient = Patient()
    print(data_replace)
    print(data_replace[0]['surname'])

    return jsonify({'success': 'True'})




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
    
    full_name = f'{data_replace[1][1]} {data_replace[2][1]} {data_replace[3][1]}'
    patient = Patient(full_name=full_name, patient_role=data_replace[0][1], surname=data_replace[1][1], first_name=data_replace[2][1], last_name=data_replace[3][1], birthday=data_replace[4][1],\
        refer=data_replace[5][1], address=data_replace[6][1], phone=data_replace[7][1], phone2=data_replace[8][1], lr_surname=data_replace[9][1],\
        lr_f_name=data_replace[10][1], lr_l_name=data_replace[11][1], lr_status=data_replace[12][1], lr_pass_num=data_replace[13][1], lr_pass_serial=data_replace[14][1],\
        lr_pass_date=data_replace[15][1], lr_pass_issued=data_replace[16][1], num_fetus=data_replace[17][1], estimated_birthday=data_replace[18][1], comment=data_replace[19][1])
    db.session.add(patient)
    db.session.commit()
    return jsonify({'success': 'True'})
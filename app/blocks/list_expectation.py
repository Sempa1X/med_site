import re
from sqlalchemy.sql.expression import false
from werkzeug.datastructures import RequestCacheControl
from app.blocks.reception import record
import datetime, json

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request, Response
from flask_login import login_required
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record, List_expectation
from app.src import age


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
current_time = str(now.strftime('%H:%M'))
bp_list_expectation = Blueprint('list_expectation', __name__, url_prefix='/list_expectation')


@bp_list_expectation.route('/', methods=['GET'])
@login_required
def list_expectation(): 
    return render_template('list_expectation/list_expectation.html')


@bp_list_expectation.route('/added', methods=['POST'])
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


@bp_list_expectation.route('/record_list', methods=['POST'])
@login_required 
def list_record():
    buffer = []
    records = []
    for i in List_expectation.query.all():
        buffer.append([i.id, i.is_pregnancy, i.full_name, i.phone, i.date_request])
    buffer = list(sorted(buffer, key=lambda i: int(i[0]), reverse=True))
    for i in buffer:
        records.append({'id': i[0], 'is_pregnancy': i[1], 'full_name': i[2], 'phone': i[3], 'date': i[4]})
    return jsonify({'success': 'true', 'records': records}) if len(records) > 0 else  jsonify({'success': 'false'})


@bp_list_expectation.route('/add_list', methods=['POST'])
@login_required 
def list_add(): 
    print(request.form)
    if request.form['check'] == 'true':
        list = List_expectation(is_pregnancy=1, full_name=request.form['full_name'], phone=request.form['phone'])
    else:
        list = List_expectation(is_pregnancy=0, full_name=request.form['full_name'], phone=request.form['phone'])
    db.session.add(list)
    db.session.commit()
    return render_template('list_expectation/list_expectation.html')


@bp_list_expectation.route('/del_list', methods=['POST'])
@login_required
def list_del(): 
    try:
        list = List_expectation.query.get(request.form['rec_id'])
        print(list.id)
        db.session.delete(list)
        db.session.commit()
        return jsonify({'success': 'true'})
    except Exception as e:
        print(e)
        return jsonify({'success': 'false'})


@bp_list_expectation.route('/is_pregnancy', methods=['POST'])
@login_required
def is_pregnancy():
    status = True
    list = List_expectation.query.get(request.form['rec_id'])
    print(request.form['check'])
    if request.form['check'] == 'true':
        list.is_pregnancy = True 
    elif request.form['check'] == 'false':
         list.is_pregnancy = False
         status = False
    db.session.commit()
    return jsonify({'success': status})

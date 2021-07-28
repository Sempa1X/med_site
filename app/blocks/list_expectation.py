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
    if 'is_pregnancy' in request.form:
        list = List_expectation(is_pregnancy=1, full_name=request.form['full_name'], phone=request.form['phone'])
        db.session.add(list)
        db.session.commit()
    else:
        list = List_expectation(is_pregnancy= 0, full_name=request.form['full_name'], phone=request.form['phone'])
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

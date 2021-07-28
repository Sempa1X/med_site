from sqlalchemy.sql.expression import false
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


@bp_list_expectation.route('/record_list', methods=['get','POST'])
@login_required 
def list_record():
    records = []
    for i in List_expectation.query.all():
        records.append({'id': i.id, 'is_pregnancy': i.is_pregnancy, 'full_name': i.full_name, 'phone': i.phone, 'date': i.date_request})
    return jsonify({'success': 'true', 'records': records}) if len(records) > 0 else  jsonify({'success': 'false'})


@bp_list_expectation.route('/add_list', methods=['POST'])
@login_required 
def list_add(): 
    return jsonify({'success': 'true'})


@bp_list_expectation.route('/del_list', methods=['POST'])
@login_required
def list_del(): 
    try:
        db.session.query(list_expectation).filter(list_expectation.id == request.form['rec_id']).delete()
        db.session.commit()
        return jsonify({'success': 'true'})
    except Exception:
        return jsonify({'success': 'false'})


@bp_list_expectation.route('/is_pregnancy', methods=['POST'])
@login_required
def is_pregnancy():
    status = True
    list = List_expectation.query.get(request.form['rec_id'])
    if request.form['check'] == True:
        list.is_pregnancy = True 
    else:
         list.is_pregnancy = False
         status = False
    db.session.commit()
    return jsonify({'success': status})

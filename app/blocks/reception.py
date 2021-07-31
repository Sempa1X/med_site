import datetime
import json

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record


now = datetime.datetime.now()
current_time = str(now.strftime('%H:%M'))
bp_reception = Blueprint('receptions', __name__, url_prefix='/reception')


# Work
@bp_reception.route('/')
@login_required
def reception():   
    return render_template('reception/reception.html')


# Work
@bp_reception.route('/add_schedule', methods=["POST"])
@login_required
def add_schedule():
    for i in request.form:
        data = json.loads(i)['data']
    is_added = False 
    for i in data:
        record = Record(doctor_id=i[0], date=i[1], time=i[2], office=i[3], doctor_full_name=i[4])
        db.session.add(record)
        db.session.commit()
        is_added = True
    return render_template('reception/reception.html') if is_added else jsonify({'success': 'false'}) 
        
    
@bp_reception.route('/get_doctors', methods=["POST"])
@login_required
def get_doctors():
    patient_data = []
    current_date = request.form['date']
    current_date_obj = now.strptime(current_date, '%d.%m.%Y')
    data_list = []
    doctors = User.query.filter(and_(User.role == 'doctor'))
    all_patients = Patient.query.all()
    for i in all_patients:
        patient_data.append({ 'patient_full_name': i.full_name, 'patient_id': i.id})
    for i in doctors:
        rec_data = []
        for o in i.records: 
            date_obj = now.strptime(o.date, '%d.%m.%Y')
            if date_obj == current_date_obj and i.id == o.doctor_id:
                rec_data.append({'rec_id': o.id, 'is_active': o.isActive, 'office': o.office, 'date': o.date, 'time': o.time,  'patient_full_name': o.patient_full_name, 'patient_id': o.patient_id})  
        data_list.append({'doc_id': i.id, 'doc_full_name': i.full_name, 'records': rec_data})
    return jsonify({'success': 'true', 'data': data_list, 'patients': patient_data, 'role': current_user.role}) if len(data_list) > 0 else jsonify({'success': 'false'})


@bp_reception.route('/is_active', methods=["POST"])
@login_required
def is_active():
    try:
        rec = Record.query.get(request.form['rec_id'])
        rec.isActive = '0'
        patient = Patient.query.get(rec.patient_id)
        patient.trust_factor = int(request.form['type'])
        db.session.commit()
        return jsonify({'success': 'true'})
    except Exception as e:
        return jsonify({'success': 'false'})


@bp_reception.route('/record', methods=["POST"])
@login_required
def record():
    try:
        rec = Record.query.get(request.form['rec_id'])
        rec.patient_full_name = request.form['patient_full_name']
        rec.patient_id = request.form['patient_id']
        db.session.commit()
        return jsonify({'success': 'true'})
    except Exception as e:
        return jsonify({'success': 'false'})


@bp_reception.route('/replace', methods=["POST"])
@login_required
def replace():
    try:
        rec = Record.query.get(request.form['rec_id'])
        rec.patient_full_name = ''
        rec.patient_id = ''
        db.session.commit()
        return jsonify({'success': 'true'})
    except Exception as e:
        print(e)
        return jsonify({'success': 'false'})
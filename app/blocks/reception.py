import datetime
import json

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record, Office


now = datetime.datetime.now()
current_time = str(now.strftime('%H:%M:%S'))
current_date = str(now.strftime('%d.%m.%Y'))
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
    

@bp_reception.post('/get_data')
@login_required
def get_data():
    # request.form['date']
    all_data = {}
    all_data['amount'] = Office.query.count()
    all_patient = []
    doctors = []
    for doctor in User.query.filter_by(role='doctor'):
        doctors.append({'name': doctor.full_name, 'id': doctor.id})

    for patient in Patient.query.all():
        all_patient.append({'patient_full_name': patient.full_name, 'patient_id': patient.id, 'trust_factor': patient.trust_factor})
    
    for office in Office.query.all():
        all_data[str(office.number)] = {'doctor': {}, 'records': [], 'name': office.name}
    for _ in Record.query.filter_by(date=request.form['date']):
        all_data[str(_.office)]['doctor'] = {'doctor_full_name': _.doctor_full_name, 'doc_id': _.doctor_id}
        all_data[str(_.office)]['records'].append({'is_true': _.is_true, 'phone': _.patient_phone, 'rec_id': _.id, 'doctor_full_name': _.doctor_full_name, 'doctor_id': _.doctor_id, 'patient_full_name':_.patient_full_name, 'patient_id':_.patient_id, 'time': _.time, 'is_active': _.isActive, 'date': _.date})
    return jsonify({'success': 'true', 'data': all_data, 'patients': all_patient, 'doctors': doctors, 'role': current_user.role})


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
        print(e)
        return jsonify({'success': 'false'})


@bp_reception.route('/record', methods=["POST"])
@login_required
def record():
    try:
        patient = Patient.query.filter_by(id=request.form['patient_id']).first()
        print(request.form['patient_id'])
        rec = Record.query.get(request.form['rec_id'])
        rec.patient_full_name = request.form['patient_full_name']
        rec.patient_id = request.form['patient_id']
        rec.patient_phone = patient.phone
        db.session.commit()
        return jsonify({'success': 'true'})
    except Exception as e:
        print(e)
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
import datetime
import json

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request
from flask_login import login_required
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
@bp_reception.route('/add_schedule', methods=['get', "POST"])
def add_schedule():
    data = [[1, '2021-07-26', '16:30', 2], [1, '2021-07-26', '16:00', 2], [1, '2021-07-26', '13:30', 2], [1, '2021-07-26', '15:30', 2]]     # request.form['data']
    is_added = False 
    for i in data:
        record = Record(doctor_id=i[0], date=i[1], time=i[2], office=i[3])
        db.session.add(record)
        db.session.commit()
        is_added = True
    return jsonify({'success': 'true'}) if is_added else jsonify({'success': 'flase'}) 
        
    
@bp_reception.route('/get_doctors', methods=["POST"])
def get_doctors():
    current_date = request.form['date']
    current_date_obj = now.strptime(current_date, '%Y-%m-%d')
    data_list = []
    rec_data = []
    doctors = User.query.filter(and_(User.role == 'doctor'))
    for i in doctors:
        for o in i.records: 
            date_obj = now.strptime(o.date, '%Y-%m-%d')
            if date_obj == current_date_obj and i.id == o.doctor_id:
                rec_data.append([{'rec_id': o.id, 'office': o.office, 'date': o.date, 'time': o.time, 'patient_full_name':o.patient_full_name, 'patient_id': o.patient_id}])  
        data_list.append({'doc_id': i.id, 'doc_full_name': i.full_name, 'records': rec_data}) 
    print(data_list)
    return jsonify({'success': 'true', 'data': data_list}) if len(data_list) > 0 else jsonify({'success': 'false'})
   
# Work
@bp_reception.route('/reception_process', methods=["POST"])
def reception_process():
    record = Record.query.filter(Record.date == request.form['date'])
    patient_info = []
    for i in record:
        patient = Patient.query.get(i.patient_id)
        patient_info.append({'full_name': patient.full_name, 'trust_factor': patient.trust_factor, 'role': patient.patient_role, 'comment': patient.comment, 'phone': patient.phone}) 
    if len(patient_info) == 0:
        return jsonify({'success': 'false'})
    return jsonify({'success': 'true', 'data': patient_info})



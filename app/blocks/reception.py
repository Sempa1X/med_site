import datetime

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request
from flask_login import login_required
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
current_date_obj = now.strptime(current_date, '%Y-%m-%d')
current_time = str(now.strftime('%H:%M'))
bp_reception = Blueprint('receptions', __name__, url_prefix='/reception')


# Work
@bp_reception.route('/')
@login_required
def reception():   
    return render_template('reception/reception.html')


# Work
@bp_reception.route('/add_schedule', methods=["POST"])
def add_schedule():
    data = [[1, '2021-07-26', '16:30', 2], [1, '2021-07-26', '16:00', 2], [1, '2021-07-26', '13:30', 2], [1, '2021-07-26', '15:30', 2]]     # request.form['data']
    is_added = False 
    ##### debug ######
    for i in data:
        print(i)
    ##################
    for i in data:
        record = Record(doctor_id=i[0], date=i[1], time=i[2], office=i[3])
        db.session.add(record)
        db.session.commit()
        is_added = True
    return jsonify({'success': 'true'}) if is_added else jsonify({'success': 'flase'}) 
        
    
@bp_reception.route('/get_doctors', methods=['get', "POST"])
def get_doctors():
    data_list = []
    doctors = User.query.filter(and_(User.role == 'doctor'))
    
    for i in doctors:
        for o in i.records:
            date_obj = now.strptime(o.date, '%Y-%m-%d')
            if date_obj == current_date_obj:
                data_list.append({'doc_full_name': i.full_name, 'office': o.office, 'date': o.date, 'time': o.time, 'patient_full_name': o.patient_full_name, 'id_patient': o.patient_id})
    return jsonify({'success': 'true', 'data': data_list}) if len(data_list) > 0 else jsonify({'success': 'false'})
   
    # doctors = []
    # res = User.query.filter(and_(User.role == 'doctor'))
    # records_list = []
    # for doctor in res:
    #     for rec in doctor.records:
    #         date = rec.date
    #         date_obj = now.strptime(date, '%Y-%m-%d')
    #         if date_obj == current_date_obj and doctor.id == rec.doctor_id:
    #             print(doctor.id, rec.doctor_id)
    #             records_list.append({'patient_id': rec.patient_id, 'patient_full': rec.patient_full_name, 'date': rec.date, 'time': rec.time, 'office': rec.office})
    #             print(records_list)
    #     doctors.append({'doc_full_name': doctor.full_name, 'doc_id': doctor.id, 'records': records_list})
    #     records_list = []
    # return jsonify({'success': 'true', 'doctors': doctors}) if len(doctors) > 0 else jsonify({'success': 'false'})


# not needed may be
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



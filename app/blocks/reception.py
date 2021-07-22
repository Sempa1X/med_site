import datetime

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request
from flask_login import login_required
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
current_time = str(now.strftime('%H:%M'))
bp_reception = Blueprint('receptions', __name__, url_prefix='/reception')


@bp_reception.route('/')
@login_required
def reception(): 
    return render_template('reception/reception.html')


@bp_reception.route('/get_doctors', methods=["POST"])
def get_doctors():
    doctors = []
    res = User.query.filter(and_(User.role == 'doctor', User.records.any(date = current_date)))

    for doctor in res:
        for rec in doctor.records:
            doctors.append({'doc_full_name': doctor.full_name, 'doc_id': doctor.id}, {'patient_id': rec.patient_id, 'patient_full': rec.patient_full_name, 'date': rec.date, 'time': rec.time, 'office': rec.office})
    return jsonify({'success': 'true', 'doctors': doctors}) if len(doctors) > 0 else jsonify({'success': 'false'})
    

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



import datetime, json

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request, Response
from flask_login import login_required
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
current_time = str(now.strftime('%H:%M'))
bp_search = Blueprint('search', __name__, url_prefix='/search')


@bp_search.route('/', methods=['POST', 'GET'])
@login_required
def search(): 
    patients = Patient.query.all()
    return render_template('search/search.html', patients=patients)


@bp_search.route('/search_process', methods=['POST'])
def search_process():
    search = request.form.get('data')
    if search:
        patient_info = []
        patients_search = Patient.query.filter(or_(Patient.full_name.contains(search), Patient.phone.contains(search), Patient.phone2.contains(search)))
        for i in patients_search:
            for o in i.records:
                patient_info.append({'full_name': i.full_name, 'trust_factor': i.trust_factor, 'role': i.patient_role, 'phone': i.phone, 'records': {'id': o.id, 'doctor_full_name':o.doctor_full_name, 'date':o.date, 'time':o.time, 'doctor_id':o.doctor_id,}}) 
        return jsonify({'success': 'false', 'text': 'Нет пациента'}) if len(patient_info) == 0 else jsonify({'success': 'true', 'patients': patient_info})
    return jsonify({'success': 'false', 'text': 'Нет пациента'})
    



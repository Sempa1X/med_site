import datetime, json

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request, Response
from flask_login import login_required
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record
from app.src import age


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
obj_current_date = now.strptime(current_date, '%Y-%m-%d')
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
        future_rec = []
        lost_rec = []
        patients_search = Patient.query.filter(or_(Patient.full_name.contains(search), Patient.phone.contains(search), Patient.phone2.contains(search)))
        for i in patients_search:
            for o in i.records:
                obj_date = now.strptime(o.date, '%d.%m.%Y')
                if obj_date >= obj_current_date:
                    future_rec.append({'id': o.id, 'is_active': o.isActive, 'doctor_full_name':o.doctor_full_name, 'date':o.date, 'time':o.time, 'office':o.office,  'doctor_id':o.doctor_id})
                else:
                    lost_rec.append({'id': o.id, 'is_active': o.isActive, 'doctor_full_name':o.doctor_full_name, 'date':o.date, 'time':o.time, 'office':o.office,  'doctor_id':o.doctor_id})
            patient_info.append({'id': i.id,'address': i.address, 'estimated_birthday': i.estimated_birthday, 'num_fetus': i.num_fetus, 'lr_pass_issued': i.lr_pass_issued, 'lr_pass_date': i.lr_pass_date, 'lr_pass_num': i.lr_pass_num, 'lr_pass_serial': i.lr_pass_serial, 'lr_status': i.lr_status, 'lr_full_name':"{} {} {}".format(i.lr_surname, i.lr_f_name, i.lr_l_name),'is_reception': i.is_reception,'birthday': i.birthday, 'full_name': i.full_name, 'comment': i.comment,'trust_factor': i.trust_factor, 'role': i.patient_role, 'phone': i.phone, 'phone2': i.phone2, 'lost_records': lost_rec, 'future_records': future_rec, 'age': age.calculate_age(int(i.birthday.split(".")[2]), int(i.birthday.split(".")[1]), int(i.birthday.split(".")[0]))}) 
        return jsonify({'success': 'false', 'text': 'Нет пациента'}) if len(patient_info) == 0 else jsonify({'success': 'true', 'patients': patient_info})
    return jsonify({'success': 'false', 'text': 'Нет пациента'})


@bp_search.post('/edit_patient')
def edit_patient():
    try:
        for patient in Patient.query.get(request.form['id']):
            patient.patient_role = request.form['type']
            patient.birthday = request.form['birthday']
            # patient.trust_factor = request.form['trust']
            patient.phone = request.form['phone']
            patient.phone2 = request.form['phone2']
            patient.first_name = request.form['first_name']
            patient.last_name = request.form['middlename']
            patient.surname = request.form['surname']
            patient.full_name =  f"{request.form['surname']} {request.form['first_name']} {request.form['middlename']}"
            patient.address = request.form['address']
            patient.comment = request.form['comment']
            patient.email = request.form['email']
            # patient.card_number = request.form['card_number']
            patient.out_to_town = request.form['out_to_town']
            patient.lr_pass_serial = request.form['lr_pass_serial']
            patient.lr_pass_num = request.form['lr_pass_num']
            patient.lr_pass_date = request.form['lr_pass_date']
            patient.lr_pass_issued = request.form['lr_pass_issued']
            if request.form['type'] == 'pregnant':
                patient.estimated_birthday = request.form['estimated_date']
                patient.num_fetus = request.form['num_fetus']
            elif request.form['type'] == 'child':
                patient.lr_f_name = request.form['lr_f_name']
                patient.lr_l_name = request.form['lr_l_name']
                patient.lr_surname = request.form['lr_surname']
                patient.lr_status = request.form['lr_status']
            db.session.commit()
            return jsonify({'success': 'true'})
    except Exception as e:
        print(e)
        return jsonify({'success': 'false'})


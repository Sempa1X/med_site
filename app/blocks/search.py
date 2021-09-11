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
    data_replace = []
    for i in request.form:
        
        data_replace.append([i, request.form[i]])
    try:
        full = f"{data_replace[0][1]} {data_replace[1][1]} {data_replace[2][1]}"
        data = f"""
        surname : {data_replace[0][1]}
        first_name : {data_replace[1][1]}
        last_name : {data_replace[2][1]}
        full_name : {full}
            
        birthday : {data_replace[3][1]}
        address : {data_replace[5][1]}
        phone : {data_replace[6][1]}
        phone2 : {data_replace[7][1]}
        card_number : {data_replace[8][1]}
        email : {data_replace[9][1]}
        out_to_town : {data_replace[10][1]}
        lr_surname : {data_replace[11][1]}
        lr_f_name : {data_replace[12][1]}
        lr_l_name : {data_replace[13][1]}
        lr_status : {data_replace[14][1]}
        lr_pass_num : {data_replace[15][1]}
        lr_pass_serial : {data_replace[16][1]}
        lr_pass_date : {data_replace[17][1]}
        lr_pass_issued : {data_replace[18][1]}
        num_fetus : {data_replace[19][1]}
        estimated_birthday : {data_replace[20][1]}
        comment : {data_replace[21][1]}
        """
        print(data)

        patient = Patient.query.get(data_replace[-1][1])
        patient.surname = data_replace[0][1]
        patient.first_name = data_replace[1][1]
        patient.last_name = data_replace[2][1]
        patient.full_name =  full
        patient.birthday = data_replace[3][1]
        patient.address = data_replace[5][1]
        patient.phone = data_replace[6][1]
        patient.phone2 = data_replace[7][1]
        patient.card_number = data_replace[8][1]
        patient.email = data_replace[9][1]
        patient.out_to_town = data_replace[10][1]
        patient.lr_surname = data_replace[11][1]
        patient.lr_f_name = data_replace[12][1]
        patient.lr_l_name = data_replace[13][1]
        patient.lr_status = data_replace[14][1]
        patient.lr_pass_num = data_replace[15][1]
        patient.lr_pass_serial = data_replace[16][1]
        patient.lr_pass_date = data_replace[17][1]
        patient.lr_pass_issued = data_replace[18][1]
        patient.num_fetus = data_replace[19][1]
        patient.estimated_birthday = data_replace[20][1]
        patient.comment = data_replace[21][1]
        #patient.patient_role = data_replace[0][1]
        db.session.commit()
        return jsonify({'success': 'true'})
    except Exception as e:
        print(e)
        return jsonify({'success': 'false'})


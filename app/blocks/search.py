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


def get_person_age(date_birth, date_today):
    years_diff = date_today.year - date_birth.year
    months_diff = date_today.month - date_birth.month
    days_diff = date_today.day - date_birth.day
    age_in_days = (date_today - date_birth).days

    age = years_diff
    age_string = str(age) + " years"

    # age can be in months or days.
    if years_diff == 0:
        if months_diff == 0:
            age = age_in_days
            age_string = str(age) + " days"
        elif months_diff == 1:
            if days_diff < 0:
                age = age_in_days
                age_string = str(age) + " days"
            else:
                age = months_diff
                age_string = str(age) + " months"
        else:
            if days_diff < 0:
                age = months_diff - 1
            else:
                age = months_diff
            age_string = str(age) + " months"
    # age can be in years, months or days.
    elif years_diff == 1:
        if months_diff < 0:
            age = months_diff + 12
            age_string = str(age) + " months" 
            if age == 1:
                if days_diff < 0:
                    age = age_in_days
                    age_string = str(age) + " days" 
            elif days_diff < 0:
                age = age-1
                age_string = str(age) + " months"
        elif months_diff == 0:
            if days_diff < 0:
                age = 11
                age_string = str(age) + " months"
            else:
                age = 1
                age_string = str(age) + " years"
        else:
            age = 1
            age_string = str(age) + " years"
    # The age is guaranteed to be in years.
    else:
        if months_diff < 0:
            age = years_diff - 1
        elif months_diff == 0:
            if days_diff < 0:
                age = years_diff - 1
            else:
                age = years_diff
        else:
            age = years_diff
        age_string = str(age) + " years"

    if age == 1:
        age_string = age_string.replace("years", "year").replace("months", "month").replace("days", "day")

    return age_string


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
                if o.date > current_date:
                    future_rec.append({'id': o.id, 'is_active': o.isActive, 'doctor_full_name':o.doctor_full_name, 'date':o.date, 'time':o.time, 'office':o.office,  'doctor_id':o.doctor_id})
                else:
                    lost_rec.append({'id': o.id, 'is_active': o.isActive, 'doctor_full_name':o.doctor_full_name, 'date':o.date, 'time':o.time, 'office':o.office,  'doctor_id':o.doctor_id})
            patient_info.append({'age': get_person_age(i.birthday, now), 'address': i.address, 'estimated_birthday': i.estimated_birthday, 'num_fetus': i.num_fetus, 'lr_pass_issued': i.lr_pass_issued, 'lr_pass_date': i.lr_pass_date, 'lr_pass_num': i.lr_pass_num, 'lr_pass_serial': i.lr_pass_serial, 'lr_status': i.lr_status, 'lr_full_name': i.lr_surname + " " + i.lr_l_name + " " + i.lr_f_name,'is_reception': i.is_reception,'birthday': i.birthday, 'full_name': i.full_name, 'comment': i.comment,'trust_factor': i.trust_factor, 'role': i.patient_role, 'phone': i.phone, 'phone2': i.phone2, 'lost_records': lost_rec, 'future_records': future_rec}) 
        return jsonify({'success': 'false', 'text': 'Нет пациента'}) if len(patient_info) == 0 else jsonify({'success': 'true', 'patients': patient_info})
    return jsonify({'success': 'false', 'text': 'Нет пациента'})
    



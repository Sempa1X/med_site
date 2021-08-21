import datetime

from flask import Blueprint, render_template, redirect,\
    url_for, request, flash, jsonify
from sqlalchemy import or_, and_
from flask_login import current_user, login_required

from app import application
from app.src.database import Record


bp_inter = Blueprint('inter', __name__, url_prefix='/interview')
dt_fmt = '%d.%m.%Y'
now = datetime.datetime.now()
current_date = datetime.datetime.today().date()
# print(current_date)

def get_records():
    records = {'today': [], 'next': []}
    for record in Record.query.filter_by(isActive='1'):
        obj_data = datetime.datetime.strptime(record.date, '%d.%m.%Y').date()
        if record.patient_id:
            if obj_data == current_date:
                records['today'].append([record.date, record.time, record.patient_phone,\
                                         record.patient.full_name, record.doctor.full_name, record.office])
            if obj_data < current_date + datetime.timedelta(days=3) and obj_data > current_date:
                records['next'].append([record.date, record.time, record.patient_phone,\
                                         record.patient.full_name, record.doctor.full_name, record.office])
    return records 



@bp_inter.route('/')
@login_required
def interview():
    records = get_records()
    return render_template("interview/interview.html", records=records)


@bp_inter.post('/')
@login_required
def interview_post():
    records = get_records()
    if records['today'] == '[]' and records['next'] == '[]':
        return jsonify({'success': 'false'})
    return jsonify({'success': 'true', 'records': records})



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
bp_search = Blueprint('search', __name__, url_prefix='/search')


@bp_search.route('/', methods=['POST', 'GET'])
@login_required
def search(): 
    patients = Patient.query.all()
    if request.method == 'POST' and 'q' in request.args or 'q' in request.form:
        is_patients = True
        search = request.form.get('q')
        patients_search_arr = []
        patients_search = Patient.query.filter(or_(Patient.full_name.contains(search), Patient.phone.contains(search), Patient.phone2.contains(search)))
        for i in patients_search:
            patients_search_arr.append(i)
        is_patients = False if len(patients_search_arr) == 0 else True
        return render_template('search/search.html',patients=patients, patients_search=patients_search, is_patients=is_patients)
    return render_template('search/search.html', patients=patients)


# @bp_search.route('/search_process', methods=['POST'])
# def search_process():
#     if 'search' in request.form and request.args.get('q'):
#         q = request.args.get('q')
#         patients = Patient.query.filter(or_(Patient.full_name.contains(q), Patient.phone.contains(q), Patient.phone2.contains(q)))
#         if len(patients) == 0:
#             return jsonify({'success': 'true', 'patients': patients})
#     return jsonify({'success': 'false', 'text': 'Нет пациента'})



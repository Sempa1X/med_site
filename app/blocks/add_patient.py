from flask import Blueprint, render_template, redirect,\
    url_for, request, flash, jsonify
from sqlalchemy import or_
from flask_login import current_user, login_user,\
    login_required, logout_user

from app import db
from app.src.database import Patient


bp_add = Blueprint('add', __name__, url_prefix='/add_patient')


@bp_add.route('/', methods=['POST', 'GET'])
@login_required
def add_patient():
    # is_found = False
    # if request.method == 'POST': 
    #     check = []
    #     full_name = request.form['sur'] + request.form['first'] + request.form['last'] 
    #     check_patient = Patient.query.filter(or_(Patient.full_name.contains(full_name), Patient.phone.contains(request.form['phone']),Patient.phone2.contains(request.form['phone2']), Patient.phone2.contains(request.form['phone']),Patient.phone.contains(request.form['phone2'])) )
    #     [check.append(i.full_name) for i in check_patient]
    #     is_found = False if len(check) == 0 else True 
    #     print(request.form['role'])
    #     if is_found:
    #         flash("Такой пацтент есть!")  
    #     else:
    #         if request.form['role'] == 'default':
    #             patient = Patient(first_name=request.form['first'], last_name=request.form['last'], surname=request.form['sur'], full_name=full_name, birthday=request.form['birthday'], refer=request.form['how_think'],\
    #                 lr_pass_serial=request.form['lr_pass_serial'], lr_pass_num= request.form['lr_pass_num'], lr_pass_date=request.form['lr_pass_date'],lr_pass_issued= request.form['lr_pass_issued'],\
    #                 comment=request.form['comment'])
    #             db.session.add(patient)
    #             db.session.commit()     
    #         elif request.form['role'] == 'pregnant':
    #             pass
    #         elif request.form['role'] == 'child':
    #             pass
    return render_template('add_patient/add_patient.html')



@bp_add.route('/added', methods=['POST'])
@login_required
def added():
    return jsonify({'success': 'false'})
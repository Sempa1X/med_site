from flask import Blueprint, render_template, redirect,\
    url_for, request, flash
from sqlalchemy import or_
from flask_login import current_user, login_user,\
    login_required, logout_user

from app import db
from app.src.database import Patient


bp_add = Blueprint('add', __name__, url_prefix='/add_patient')


@bp_add.route('/', methods=['POST', 'GET'])
@login_required
def add_patient():
    is_found = False
    if request.method == 'POST': 
        check = []
        check_birthday = []
        full_name = request.form['sur'] + " " + request.form['first'] + " "  + request.form['last'] 
        
        check_full_name = Patient.query.filter(Patient.full_name.contains(full_name)) 
        [check.append(i.full_name) for i in check_full_name]

        check_birth = Patient.query.filter(Patient.birthday.contains(request.form['birthday'])) 
        [check_birthday.append(i.full_name) for i in check_birth]
        
        is_found = False if len(check) == 0 or len(check_birthday) == 0 else True 
        
        if is_found:
            flash("Такой пацтент есть!")  
        else:
            flash("Добавлен")  
            if request.form['role'] == 'default':
                patient = Patient(first_name=request.form['first'], last_name=request.form['last'], surname=request.form['sur'], full_name=full_name, birthday=request.form['birthday'], refer=request.form['how_think'],\
                    lr_pass_serial=request.form['lr_pass_serial'], lr_pass_num= request.form['lr_pass_num'], lr_pass_date=request.form['lr_pass_date'],lr_pass_issued= request.form['lr_pass_issued'],\
                    comment=request.form['comment'])
                db.session.add(patient)
                db.session.commit()     
            
            elif request.form['role'] == 'pregnant':
                patient = Patient(first_name=request.form['first'], last_name=request.form['last'], surname=request.form['sur'], full_name=full_name, birthday=request.form['birthday'], refer=request.form['how_think'],\
                    lr_pass_serial=request.form['lr_pass_serial'], lr_pass_num= request.form['lr_pass_num'], lr_pass_date=request.form['lr_pass_date'],lr_pass_issued= request.form['lr_pass_issued'],\
                    comment=request.form['comment'], estimated_birthday=request.form['estimated_birthday'], num_fetus=request.form['num_fetus'])
                db.session.add(patient)
                db.session.commit()  
            
            elif request.form['role'] == 'child':
                patient = Patient(first_name=request.form['first'], last_name=request.form['last'], surname=request.form['sur'], full_name=full_name, birthday=request.form['birthday'], refer=request.form['how_think'],\
                    lr_pass_serial=request.form['lr_pass_serial'], lr_pass_num= request.form['lr_pass_num'], lr_pass_date=request.form['lr_pass_date'],lr_pass_issued= request.form['lr_pass_issued'],\
                    comment=request.form['comment'], lr_f_name=request.form['lr_f_name'], lr_l_name=request.form['lr_l_name'], lr_surname=request.form['lr_surname'])
                db.session.add(patient)
                db.session.commit()  
    return render_template('add_patient/add_patient.html')

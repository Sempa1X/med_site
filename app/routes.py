"""
Файл для логики путей сайта
"""
# импортируем стандартные модули
from datetime import datetime
import os

# импортируем установленные модули
from flask import redirect, url_for,\
    render_template, flash, request, g
from flask_login import current_user, login_required, \
    login_user, logout_user
from sqlalchemy import or_, and_

# импортируем свои файлы
from app import application, db, login
from app.models import Schedule, User, Record, Patient





@application.before_request
def before_request():
    pass
    # if current_user.is_authenticated:
    #     return redirect(url_for('login'))    


@application.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    doctors = User.query.filter(and_(User.isActive=='True', User.role=="doctor"))
    if request.method == 'POST':
        doctor = request.form.get('doctor')
        return redirect(url_for('schedule', doc_id=doctor))

    return render_template('main/schedule.html', doctors=doctors)


@application.route('/schedule/<doc_id>', methods=['GET', 'POST'])
@login_required
def schedule_doc(doc_id):
    schedules = Schedule.query.filter(and_(Schedule.doctor_id==doc_id, Schedule.isActive==True))
    if request.method == 'POST':
        pass
    return render_template('main/schedule_doc.html')


@application.route('/record', methods=['GET', 'POST'])
@login_required
def record_post():
    if request.method == 'POST':
        pacient_choice = request.form.get('pacient_choice')
        return redirect(url_for('record', pacient_choice=pacient_choice))
    return render_template('main/pacient_choice.html')


@application.route("/record/<pacient_choice>", methods=['GET', 'POST'])
@login_required
def record(pacient_choice):
    doctors = User.query.filter(and_(User.isActive=='True', User.role=="doctor")) # filter(and_(User.isActive=='True', User.role=="doctor"))

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        surname = request.form.get('surname')
        birthday = request.form.get('date_birth')
        how_thing = request.form.get('how_thing')
        address = request.form.get('address')
        calendar = request.form.get('calendar')
        time = request.form.get('time')
        doctor = request.form.get('doctor')
        doctor_id = request.form.get('doctor')
        doc_id = str(doctor_id).split(':')[0]
        reason = request.form.get('reason')

        if pacient_choice == 'Ребенок':
            lr_f_name = request.form.get('lr_f_name')
            lr_l_name = request.form.get('lr_l_name')
            lr_surname = request.form.get('lr_surname')
            lr_status = request.form.get('lr_status')
            lr_pass_serial = request.form.get('lr_pass_serial')
            lr_pass_num = request.form.get('lr_pass_num')
            lr_pass_date = request.form.get('lr_pass_date')
            lr_pass_issued = request.form.get('lr_pass_issued')

            pacient = Patient(first_name=first_name, last_name=last_name, surname=surname, birthday=birthday, refer=how_thing, address=address, lr_f_name=lr_f_name, lr_l_name=lr_l_name, lr_surname=lr_surname, lr_status=lr_status, lr_pass_serial=lr_pass_serial, lr_pass_num=lr_pass_num, lr_pass_date=lr_pass_date, lr_pass_issued=lr_pass_issued)
            print(first_name, last_name, surname, birthday, how_thing, address, lr_f_name, lr_l_name, lr_surname, lr_status, lr_pass_serial, lr_pass_num, lr_pass_date,  lr_pass_issued)
            db.session.add(pacient)
            db.session.commit()

            reception = Record(
                doctor=doctor,
                doctor_id=str(doc_id),
                patient_id=str(pacient.id),
                pacient=f'{last_name} {first_name} {surname}',
                date=calendar,
                time=time,
                reason=reason
            )
            db.session.add(reception)
            db.session.commit()
        
        elif pacient_choice == 'Обычный':
            pass_serial_d = request.form.get('pass_serial')
            pass_num_d = request.form.get('pass_num')
            pass_date_d = request.form.get('pass_date')
            pass_issued_d = request.form.get('pass_issued')
            
            pacient = Patient(
                first_name=first_name,
                last_name=last_name,
                surname=surname,
                birthday=birthday,
                refer=how_thing,
                address=address,
                lr_pass_serial = pass_serial_d,
                lr_pass_num = pass_num_d,
                lr_pass_date = pass_date_d,
                lr_pass_issued = pass_issued_d
            )
    
            db.session.add(pacient)
            db.session.commit()

            reception = Record(
                doctor=doctor,
                doctor_id=str(doc_id),
                patient_id=str(pacient.id),
                pacient=f'{last_name} {first_name} {surname}',
                date=calendar,
                time=time,
                reason=reason
            )
            db.session.add(reception)
            db.session.commit()

        elif pacient_choice == 'Беременная':
            pass_serial = request.form.get('pass_serial')
            pass_num = request.form.get('pass_num')
            pass_date = request.form.get('pass_date')
            pass_issued = request.form.get('pass_issued')
            count_embr = request.form.get('count_embr')
            estimated_birthday = request.form.get('estimated_birthday')

            pacient = Patient(
                first_name=first_name,
                last_name=last_name,
                surname=surname,
                birthday=birthday,
                refer=how_thing,
                address=address,
                pass_serial = pass_serial,
                pass_num = pass_num,
                pass_date = pass_date,
                pass_issued = pass_issued,
                count_embr=count_embr,
                estimated_birthday=estimated_birthday
            )

            reception = Record(
                doctor=doctor,
                doctor_id=str(doc_id),
                patient_id=str(pacient.id),
                pacient=f'{last_name} {first_name} {surname}',
                date=calendar,
                time=time,
                reason=reason
            )
            db.session.add(reception)
            db.session.commit()

        return render_template("main/doctor_record.html", pacient_choice=pacient_choice, doctors=doctors) 
    return render_template("main/doctor_record.html", pacient_choice=pacient_choice, doctors=doctors)


@application.route("/reception", methods=['GET', 'POST'])
@login_required
def reception():
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    doctors_list = User.query.filter(and_(User.isActive=='True', User.role=="doctor"))
    doctors = []

    for doctor in doctors_list:
        doctors.append(
        {
            'id': doctor.id,
            'full_name': f'{doctor.first_name} {doctor.last_name} {doctor.surname}'
        },
        )

    if request.method == 'POST' and "btn-select" in request.form:
        calendar = request.form.get('calendar')
        select_doc = request.form.get('select_doc')

        for doctor in doctors:
            for _ in range(len(doctor)): 
                ids = doctor.get('id')
 
                if select_doc == 'doctor_all':
                    records = Record.query.filter(and_(Record.date == calendar), (Record.isActive == True))
                    return render_template("main/doctor_reception.html", doctors=doctors, receptions=records, current_date=calendar) 
                elif select_doc == f'doctor_{ids}':
                    records_doctor = Record.query.filter(and_(Record.date == calendar), (Record.doctor_id == ids), (Record.isActive == True))                 
                    return render_template("main/doctor_reception.html", doctors=doctors, receptions=records_doctor, current_date=calendar) 
    
    if request.method == 'POST' and 'btn-close' in request.form:
        radio = request.form.get('radioBTN')
        records_2 = Record.query.all()

        for i in records_2:
            if radio == None:
                flash('Не выбрано действие', "primary")
            
            elif radio == f"option_true_{i.patient_id}":
                flash('Пациент пришел', "success")
                pacient = Patient.query.get(i.patient_id)
                pacient.reception = False
                i.trust = False
                i.isActive = False
                db.session.commit()
                

            elif radio == f"option_false_{i.patient_id}":
                flash('Пациент не пришел', "primary") 
                pacient = Patient.query.get(i.patient_id)
                pacient.trust_factor = False
                pacient.reception = False
                i.trust = False
                i.isActive = False
                db.session.commit()
                    
        
    return render_template("main/doctor_reception.html", doctors=doctors, current_date=current_date) #, pac_id=pacient_id, receptions=reasons, doctors=doctors, current_date=current_date, doc_id=doc_id)

@application.route("/test", methods=['GET', 'POST'])
@login_required
def test():
        
    return render_template("main/timetable.html")


# обработка станицы авторизации 
@application.route('/', methods=['GET', 'POST'])
def login():
    # если пользователя авторизован, перенаправить на главную
    if current_user.is_authenticated:
        return redirect(url_for('reception'))
    # если на отправили форму
    if request.method == 'POST':
        # получаем пользователя
        user = User.query.filter_by(username=request.form.get('username')).first()
        # Если username или пароль не верны, то вывести сообщение и обновить страницу
        if user is None or not user.check_password(request.form.get('password')):
            flash('Пароль или имя пользователя не верны!')
            return redirect(url_for('login'))
        # авторизуем пользователя и перенаправляем на главную
        login_user(user)
        return redirect(url_for('reception'))
    return render_template('main/login.html', title='Золотые ручки - Авторизация')


# обработка станицы регистрации
@application.route('/register_staff', methods=['GET', 'POST'])
def register():
    # ксли пользователь авторизован перенаправляем на главню
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    # если отправили форму
    if request.method == 'POST':
        # добавляем пользователя и отправляем сообщение и перенаправляем на авторизацию
        user = User(username=request.form.get('username'), email=request.form.get('email'))
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрирваны!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Золотые ручки - Регистрация')


# обработка станицы деавторизации
@application.route('/logout')
@login_required
def logout():
    logout_user() # деавторизация и переходим на авторизацию
    return redirect(url_for('login'))


# обработка станицы 404
@application.errorhandler(404)
@login_required
def error_404(error):
    return render_template("main/404.html", error=error)








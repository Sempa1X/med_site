import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
current_time = str(now.strftime('%H:%M'))


class User(UserMixin, db.Model):
    __tablename__ = 'personal'
 
    id = db.Column(db.Integer, primary_key=True, unique=True) 
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    full_name = db.Column(db.String(255))

    sex = db.Column(db.String(255), default=1)
    birthday = db.Column(db.String(50))

    phone = db.Column(db.String(50))
    phone2 = db.Column(db.String(50))
    email = db.Column(db.String(255))

    reg_time = db.Column(db.String(255), index=True, default=current_date + " " + current_time)
    coment = db.Column(db.String(255))

    division = db.Column(db.String(255))    
    certificate = db.Column(db.String(255))
    role = db.Column(db.String(255), default='doctor')

    records = db.relationship('Record', backref='doctor')
    is_active = db.Column(db.Boolean, default=True)

    # метод для установки пароля пользователю
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # метод для проверки пароля пользователя
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    full_name = db.Column(db.String(255))

    birthday = db.Column(db.String(50))
    refer = db.Column(db.String(255), default='Сарафан')

    is_reception = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(50))
    phone2 = db.Column(db.String(50))

    lr_f_name = db.Column(db.String(255))
    lr_l_name = db.Column(db.String(255))
    lr_surname = db.Column(db.String(255))
    lr_status = db.Column(db.String(255))

    lr_pass_serial = db.Column(db.String(255))
    lr_pass_num = db.Column(db.String(255))
    lr_pass_date = db.Column(db.String(255))
    lr_pass_issued = db.Column(db.String(255))

    address = db.Column(db.String(255))
    trust_factor = db.Column(db.Boolean, default=True)
    patient_role = db.Column(db.String(255))
    estimated_birthday = db.Column(db.String(255))
    num_fetus = db.Column(db.Integer, default=1)

    speed = db.Column(db.Boolean, default=False)
    comment = db.Column(db.String(255))
    email = db.Column(db.String(255))
    card_number = db.Column(db.Integer)
    out_to_town = db.Column(db.String(255))

    records = db.relationship('Record', backref='patient')


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)

    doctor_full_name = db.Column(db.String(255))
    doctor_id = db.Column(db.Integer, db.ForeignKey('personal.id'))
    
    patient_full_name = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    patient_phone = db.Column(db.String(50))
    
    date = db.Column(db.String(255), index=True)
    time = db.Column(db.String(255), index=True)
    isActive = db.Column(db.String(255), default='1')
    comment = db.Column(db.String(255))
    office = db.Column(db.Integer())
    is_true = db.Column(db.Integer(), default=1)
    is_send = db.Column(db.String(255), index=True, default='0')
    is_interview = db.Column(db.Integer(), default=0)
    is_go = db.Column(db.Boolean(), default=1)


class Office(db.Model):
    __tablename__ = 'offices'
    id = db.Column(db.Integer, primary_key=True)   
    number = db.Column(db.Integer)
    name = db.Column(db.String(255))


class List_expectation(db.Model):
    __tablename__ = 'list_expectations'
    id = db.Column(db.Integer, primary_key=True)
    is_pregnancy = db.Column(db.String(255)) # False ребенок
    full_name = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    date_request = db.Column(db.String(255), index=True, default=current_date + " " + current_time)


class Document(db.Model):
    __tablename__ = 'docs'
    id = db.Column(db.Integer, primary_key=True)  
    path = db.Column(db.String(255), unique=True)
    date = db.Column(db.String(255))
    desc = db.Column(db.String(255), default='Нет описания')


class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)  
    patient_full_name=db.Column(db.String(255), default='None')
    age=db.Column(db.String(255), default='None')
    diagnoz=db.Column(db.String(255), default='None')
    birthday=db.Column(db.String(255), default='None')
    osmotr=db.Column(db.String(255), default='None')
    end=db.Column(db.String(255), default='None')
    desc=db.Column(db.String(255), default='None')
    doctor_full_name=db.Column(db.String(255), default='None')
    apparate=db.Column(db.String(255), default='None')
    lp=db.Column(db.String(255), default='None')
    lp_full=db.Column(db.String(255), default='None')
    lp_index=db.Column(db.String(255), default='None')
    lzd=db.Column(db.String(255), default='None')
    lzs=db.Column(db.String(255), default='None')
    lzd_index=db.Column(db.String(255), default='None')
    vals=db.Column(db.String(255), default='None')
    sin=db.Column(db.String(255), default='None')
    vos=db.Column(db.String(255), default='None')
    duga=db.Column(db.String(255), default='None')
    kdo=db.Column(db.String(255), default='None')
    kso=db.Column(db.String(255), default='None')
    kdo_index=db.Column(db.String(255), default='None')
    pp=db.Column(db.String(255), default='None')
    pz=db.Column(db.String(255), default='None')
    npv=db.Column(db.String(255), default='None')
    mzp=db.Column(db.String(255), default='None')
    zs=db.Column(db.String(255), default='None')
    imm=db.Column(db.String(255), default='None')
    la=db.Column(db.String(255), default='None')
    la_mm=db.Column(db.String(255), default='None')
    fb=db.Column(db.String(255), default='None')
    fbt=db.Column(db.String(255), default='None')
    vmax=db.Column(db.String(255), default='None')
    pmax=db.Column(db.String(255), default='None')
    pmean=db.Column(db.String(255), default='None')
    ava=db.Column(db.String(255), default='None')
    regu=db.Column(db.String(255), default='None')
    vmaxMV=db.Column(db.String(255), default='None')
    pmaxMV=db.Column(db.String(255), default='None')
    pmeanMV=db.Column(db.String(255), default='None')
    mva=db.Column(db.String(255), default='None')
    regu2=db.Column(db.String(255), default='None')
    vmaxPV=db.Column(db.String(255), default='None')
    pmaxPV=db.Column(db.String(255), default='None')
    pmeanPV=db.Column(db.String(255), default='None')
    regu3=db.Column(db.String(255), default='None')
    vmaxTV=db.Column(db.String(255), default='None')
    pmaxTV=db.Column(db.String(255), default='None')
    pmeanTV=db.Column(db.String(255), default='None')
    regu4=db.Column(db.String(255), default='None')



from app import login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


















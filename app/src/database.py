import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db
from app import login


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

    records = db.relationship('Record', backref='patient')


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)

    doctor_full_name = db.Column(db.String(255))
    doctor_id = db.Column(db.Integer, db.ForeignKey('personal.id'))
    
    patient_full_name = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    
    date = db.Column(db.String(255), index=True)
    time = db.Column(db.String(255), index=True)
    trust = db.Column(db.Boolean, default=True)
    isActive = db.Column(db.Boolean, default=True)
    reason = db.Column(db.String(255))



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


















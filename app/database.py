# import modules
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))

    sex = db.Column(db.Boolean, default=1)
    birthday = db.Column(db.String(50))
    
    phone = db.Column(db.String(50))
    phone2 = db.Column(db.String(50))
    email = db.Column(db.String(50))
    
    reg_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    isActive = db.Column(db.String(50)) # Работаспособность
    isAdmin = db.Column(db.Boolean, default=0)
    isDev =  db.Column(db.Boolean, default=0)
    
    coment = db.Column(db.String(255))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Doctor( User):
    __tablename__ = "doctors"
    division = db.Column(db.String(255))
    certificate = db.Column(db.String(255))
    phone3 = db.Column(db.String(255))


class Patient(User):
    __tablename__ = 'patients'
    refer = db.Column(db.String(255))
    pacient_record = db.Column(db.String(255))
    
    lr_f_name = db.Column(db.String(255))
    lr_l_name = db.Column(db.String(255))
    lr_surname = db.Column(db.String(255))

    lr_pass_serial = db.Column(db.String(255))
    lr_pass_num = db.Column(db.String(255))
    lr_pass_date = db.Column(db.String(255))
    lr_pass_issued = db.Column(db.String(255))
    
    address = db.Column(db.String(255))
    trust_factor = db.Column(db.Boolean, default=True)


class Child(Patient):
    __tablename__ = 'childs'
    lr_status = db.Column(db.String(255))
    phone4 = db.Column(db.String(255))


class Pregnant(Patient):
    __tablename__ = 'pregnants'
    estimated_birthday = db.Column(db.String(255))
    num_fetus = db.Column(db.Integer)
    phone5 = db.Column(db.String(255))


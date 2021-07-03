# import modules
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


# create SubTable role_user
role_user = db.Table(
    'role_user',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


# Create table Role
class Role(db.Model):
    __tablename__ = 'roles'

    # add column for table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    desc = db.Column(db.String(255))

    def __repr__(self):
        return f'< Role | id:{self.id} | Name: {self.name} >'


class User(db.Model):
    __tablename__ = 'users'

    # add column for table
    id = db.Column(db.Integer, primary_key=True)
    # ФИО
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))

    sex = db.Column(db.Boolean, default=1)
    birthday = db.Column(db.String(50))
    
    phone = db.Column(db.String(50))
    phone2 = db.Column(db.String(50))
    email = db.Column(db.String(50))
    
    reg_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    isActive = db.Column(db.String(50))
    roles = db.relationship('Role', secondary=role_user, backref=db.backref('roles'), lazy='dynamic')
    
    coment = db.Column(db.String(255))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Patient(db.Model, User):
    __tablename__ = 'patients'

    lr_f_name = db.Column(db.String(50))
    lr_l_name = db.Column(db.String(50))
    lr_surname = db.Column(db.String(50))

    passport_serial = db.Column(db.String(10))
    passport_num = db.Column(db.String(50))
    passport_date = db.Column(db.String(50))
    passport_issued =  db.Column(db.String(50))

    address =  db.Column(db.String(100))
    trast = db.Column(db.Boolean, default=1)

    referal = db.Column(db.String(50))
    patient_record = db.Column(db.String(255))
    

class Doctor(db.Model, User):
    __tablename__ = 'doctors'

    spec =  db.Column(db.String(50))
    sertificate =  db.Column(db.String(50))
    
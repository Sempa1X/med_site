# import modules
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


# create SubTable role_user
role_user = db.Table(
    'role_user',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
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
    isActive = db.Column(db.String(50)) # Работаспособность
    roles = db.relationship('Role', secondary=role_user, backref=db.backref('roles'), lazy='dynamic')
    
    coment = db.Column(db.String(255))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Doctor(db.Model, User):
    __tablename__ = "doctors"
    division = db.Model
# import modules
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_required
from flask_security import RoleMixin

from app import login, db



roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    passwd = db.Column(db.String(50))

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))

    active = db.Column(db.Boolean())
    # Для получения доступа к связанным объектам
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    # Flask - Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # # sex = db.Column(db.Boolean, default=1)
    # birthday = db.Column(db.String(50))
    
    # phone = db.Column(db.String(50))
    # phone2 = db.Column(db.String(50))
    # email = db.Column(db.String(50))
    
    # reg_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # isActive = db.Column(db.String(50)) # Работаспособность
    # isAdmin = db.Column(db.Boolean, default=0)
    # isDev =  db.Column(db.Boolean, default=0)
    # division = db.Column(db.String(255))
    # certificate = db.Column(db.String(255))
    
    # # coment = db.Column(db.String(255))


# class Doctor(db.Model, UserMixin):
#     __tablename__ = "doctors"
#     id = db.Column(db.Integer, primary_key=True)

#     first_name = db.Column(db.String(20))
#     last_name = db.Column(db.String(20))
#     surname = db.Column(db.String(20))

#     birthday = db.Column(db.String(50))

#     division = db.Column(db.String(255))
#     certificate = db.Column(db.String(255))
#     phone3 = db.Column(db.String(255))

#     reg_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     isActive = db.Column(db.String(50)) # Работаспособность
#     isAdmin = db.Column(db.Boolean, default=0)

#     login = db.Column(db.String(50))
#     passwd = db.Column(db.String(50))

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)


#     def check_password(self, password):
#         return check_password_hash(self.passwd, password)


# class Patient(db.Model):
#     __tablename__ = 'patients'
#     id = db.Column(db.Integer, primary_key=True)

#     first_name = db.Column(db.String(20))
#     last_name = db.Column(db.String(20))
#     surname = db.Column(db.String(20))

#     birthday = db.Column(db.String(50))

#     refer = db.Column(db.String(255))
#     pacient_record = db.Column(db.String(255))
    
#     lr_f_name = db.Column(db.String(255))
#     lr_l_name = db.Column(db.String(255))
#     lr_surname = db.Column(db.String(255))

#     lr_pass_serial = db.Column(db.String(255))
#     lr_pass_num = db.Column(db.String(255))
#     lr_pass_date = db.Column(db.String(255))
#     lr_pass_issued = db.Column(db.String(255))
    
#     address = db.Column(db.String(255))
#     trust_factor = db.Column(db.Boolean, default=True)


# class Child(db.Model):
#     __tablename__ = 'childs'
#     id = db.Column(db.Integer, primary_key=True)

#     first_name = db.Column(db.String(20))
#     last_name = db.Column(db.String(20))
#     surname = db.Column(db.String(20))

#     birthday = db.Column(db.String(50))
#     lr_status = db.Column(db.String(255))
#     phone4 = db.Column(db.String(255))

#     refer = db.Column(db.String(255))
#     pacient_record = db.Column(db.String(255))
    
#     lr_f_name = db.Column(db.String(255))
#     lr_l_name = db.Column(db.String(255))
#     lr_surname = db.Column(db.String(255))

#     lr_pass_serial = db.Column(db.String(255))
#     lr_pass_num = db.Column(db.String(255))
#     lr_pass_date = db.Column(db.String(255))
#     lr_pass_issued = db.Column(db.String(255))
    
#     address = db.Column(db.String(255))
#     trust_factor = db.Column(db.Boolean, default=True)



# class Pregnant(db.Model):
#     __tablename__ = 'pregnants'
#     id = db.Column(db.Integer, primary_key=True)

#     first_name = db.Column(db.String(20))
#     last_name = db.Column(db.String(20))
#     surname = db.Column(db.String(20))

#     refer = db.Column(db.String(255))
#     pacient_record = db.Column(db.String(255))

#     lr_pass_serial = db.Column(db.String(255))
#     lr_pass_num = db.Column(db.String(255))
#     lr_pass_date = db.Column(db.String(255))
#     lr_pass_issued = db.Column(db.String(255))
    
#     address = db.Column(db.String(255))
#     trust_factor = db.Column(db.Boolean, default=True)

#     birthday = db.Column(db.String(50))
#     estimated_birthday = db.Column(db.String(255))
#     num_fetus = db.Column(db.Integer)
#     phone5 = db.Column(db.String(255))


@login.user_loader
@login_required
def load_user(id):
    return User.query.get(int(id))
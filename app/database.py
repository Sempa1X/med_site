# import modules
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

    roles = db.relationship('Role', secondary=role_user, backref=db.backref('roles'), lazy='dynamic')
    # Data for user




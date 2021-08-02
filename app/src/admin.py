import re
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for, request, flash

from app import db, application
from app.src.database import User


class MyAdminView(ModelView):
    excluded_list_columns = ['password_hash']
    def is_accessible(self):
        if current_user.is_authenticated == False:
            return redirect(url_for('login.login'))
        return current_user.role == 'superadmin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('receptions.reception'))


class MyIndexView(AdminIndexView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        counter = []
        if request.method == 'POST':
            check_pers = User.query.filter_by(username=request.form['username'])
            if check_pers != None:
                for i in check_pers:
                    counter.append(i.username)
                if len(counter) == 0:
                    full_name = request.form['s_name'] + " " + request.form['f_name'] + " " + request.form['l_name']
                    u = User( username=request.form['username'], first_name=request.form['f_name'], last_name=request.form['l_name'], surname=request.form['s_name'], full_name=full_name, sex=request.form.get('sex'),\
                        birthday=request.form['birthday'], phone=request.form['phone'], phone2=request.form['phone2'], email=request.form['email'], division=request.form['division'], certificate=request.form['certificate'],\
                        role=request.form.get('role'))
                    u.set_password(request.form['passwd'])

                    db.session.add(u)
                    db.session.commit()
            return self.render('admin/index.html')
        return self.render('admin/index.html')

    def is_accessible(self):
        if current_user.is_authenticated == False:
            return redirect(url_for('login.login'))
        return current_user.role == 'superadmin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('receptions.reception'))


    
from flask import render_template, redirect, url_for,\
    request, flash
from flask_admin import expose, AdminIndexView
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView


class MyAdminView(ModelView):
    def is_accessible(self):
            return (current_user.role == 'superadmin' and
                current_user.is_authenticated)
    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('login'))


    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('login'))


class MyIndexView(AdminIndexView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        from app.models import User
        if current_user.role != 'superadmin':
            return redirect(url_for('login'))
        # если отправили форму
        if request.method == 'POST':
            from app import db
            # добавляем пользователя и отправляем сообщение и перенаправляем на авторизацию
            user = User(username=request.form.get('username'), email=request.form.get('email'), role=request.form.get('role'))
            user.set_password(request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flash( f"Вы зарегистрирвали пользователя < { request.form.get('role') } | { request.form.get('username') } | { request.form.get('password') } >!")
            return redirect(url_for('admin.index'))
        return self.render('admin/index.html')

    def is_accessible(self):
        return (current_user.role == 'superadmin'  and
            current_user.is_authenticated)

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('login'))

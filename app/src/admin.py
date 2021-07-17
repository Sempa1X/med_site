import os

from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView, expose
from werkzeug.utils import secure_filename
from flask_login import current_user
from flask import redirect, url_for, request, flash

from app import db, application


UPLOAD_FOLDER = application.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class MyAdminView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.isAdmin
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login.logins'))



class MyIndexView(AdminIndexView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            return self.render('admin/index.html')
        return self.render('admin/index.html')

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.isAdmin
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login.logins'))

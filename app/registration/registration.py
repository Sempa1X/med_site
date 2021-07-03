from flask import Blueprint, redirect,\
    render_template, url_for

reg = Blueprint('reg', __name__)


@reg.route('/')
def register():
    
    return render_template('registration/reg.html', title='Medic - регистрация')


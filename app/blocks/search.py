import datetime

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify
from flask_login import login_required
from sqlalchemy import or_, and_
from werkzeug.wrappers import request

from app import db
from app.src.database import User, Patient, Record


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
current_time = str(now.strftime('%H:%M'))
bp_search = Blueprint('search', __name__, url_prefix='/search')


@bp_search.route('/')
@login_required
def search(): 
    return render_template('search/search.html')


@bp_search.post('/search_process')
def search_process():
    if 'field' in request.form and request.args.get('q'):
        q = request.args.get('q')
        patients = Patient.query.filter(or_(Patient.full_name.contains(q), Patient.phone.contains(q), Patient.phone2.contains(q)))
        return jsonify({'success': 'true', 'patients': patients})
    return jsonify({'success': 'false', 'text': 'Нет пациента'})



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
bp_reception = Blueprint('receptions', __name__, url_prefix='/reception')


@bp_reception.route('/')
@login_required
def reception(): 
    res = User.query.filter(and_(User.role == 'doctor', User.records.any(date = current_date)))
    return render_template('reception/reception.html', res=res)


@bp_reception.post('/reception_process')
def reception_process():
    if 'date' in request.form:
        record = Record(Record.date == request.form['date'])
        return jsonify({'success': 'true', 'records': record})
    return jsonify({'success': 'false', 'text': 'Нет расписания на эту дату'})



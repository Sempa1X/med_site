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
bp_schedule = Blueprint('schedule', __name__, url_prefix='/schedule')


@bp_schedule.route('/')
@login_required
def schedule(): 
    return render_template('schedule/schedule.html')


@bp_schedule.post('/schedule_process')
def schedule_process():
    if 'date' in request.form:
        record = Record(Record.date == request.form['date'])
        return jsonify({'success': 'true', 'records': record})
    return jsonify({'success': 'false', 'text': 'Нет расписания на эту дату'})



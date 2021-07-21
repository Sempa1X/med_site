import datetime

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify
from flask_login import login_required
from sqlalchemy import or_, and_
from werkzeug.wrappers import request

from app import db
from app.src.database import User, Patient, Record, Schedule


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
current_time = str(now.strftime('%H:%M'))
bp_schedule = Blueprint('schedule', __name__, url_prefix='/schedule')


@bp_schedule.route('/', methods=['GET', 'POST'])
@login_required
def schedule():
    doctors = User.query.filter(and_(User.is_active=='True', User.role=="doctor"))
    return render_template('schedule/schedule.html', doctors=doctors)



@bp_schedule.route('/process', methods=['GET', 'POST'])
@login_required
def schedule_process():
    data = request.form['data']

    for i in data:
        schedule = Schedule()
        db.session.add(schedule)
        db.session.commit()

    # return render_template('main/schedule_doc.html')

import datetime
import json

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record, Office


now = datetime.datetime.now()
current_time = str(now.strftime('%H:%M'))
bp_office = Blueprint('office', __name__, url_prefix='/office')

@bp_office.route('/add')
def add():
    
    return render_template('office/office_add.html')
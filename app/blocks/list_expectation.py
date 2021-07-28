import datetime, json

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request, Response
from flask_login import login_required
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record, List_expectation
from app.src import age


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
current_time = str(now.strftime('%H:%M'))
bp_list_expectation = Blueprint('list_expectation', __name__, url_prefix='/list_expectation')


@bp_list_expectation.route('/', methods=['GET'])
@login_required
def list_expectation(): 
    return render_template('list_expectation/list_expectation.html')


@bp_list_expectation.route('/record_list', methods=['POST'])
@login_required 
def list_get():
    status = True
    all_list_dict = []
    all_list = List_expectation.query.all()
    for i in all_list:
        all_list_dict.append(i)
    return jsonify({'success': 'true', 'all_list': all_list_dict}) if status else  jsonify({'success': 'false'})


@bp_list_expectation.route('/add_list', methods=['POST'])
@login_required 
def list_add(): 
    return jsonify({'success': 'true'})


@bp_list_expectation.route('/del_list', methods=['POST'])
@login_required
def list_del(): 
    return jsonify({'success': 'true'})


import datetime, json

from flask import Blueprint, render_template, redirect,\
    url_for, jsonify, request, Response
from flask_login import login_required
from sqlalchemy import or_, and_

from app import db
from app.src.database import User, Patient, Record
from app.src import age


now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
current_time = str(now.strftime('%H:%M'))
bp_error = Blueprint('errors', __name__, url_prefix='/')



@bp_error.errorhandler(404)
def error_404(error):
    return render_template("error/404.html", error=error)


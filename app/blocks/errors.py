from flask import Blueprint, render_template, redirect,\
    url_for, request, flash, jsonify
from sqlalchemy import or_
from flask_login import current_user

bp_error = Blueprint('errors', __name__, url_prefix='/')


@bp_error.errorhandler(404)
def error_404(error):
    return render_template("error/404.html", error=error), 404
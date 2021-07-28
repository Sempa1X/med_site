from flask import render_template

from app import application, db, login


@application.before_request
def before_request():
    pass


@application.errorhandler(404)
def error_404(error):
    return render_template("error/404.html", error=error)


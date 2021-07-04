from flask import redirect, render_template,\
    url_for, flash

from app import application as main


@main.route('/', methods=['POST', 'GET'])
def sing_in():
    return render_template('main/panel.html')


    
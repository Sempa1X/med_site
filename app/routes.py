from flask import redirect, render_template,\
    url_for, flash

from app import application as main

# main.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@main.route('/', methods=['POST', 'GET'])
def panel():
    return render_template('main/panel.html')


@main.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    return render_template('main/signup.html')
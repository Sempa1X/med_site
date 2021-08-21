import smtplib
import datetime
import time 
import os 

from flask_mail import Message


from flask import render_template
from sqlalchemy import and_
from datetime import datetime as DT, timedelta


dt_fmt = '%d.%m.%Y'
now = datetime.datetime.now()
current_time = str(now.strftime('%H:%M:%S'))
current_date = str(now.strftime('%d.%m.%Y'))


def send_emails():
    from app import application, mail
    try:
        time.sleep(2)
        msg = Message('Test', application.config['MAIL_USERNAME'], 'sempa1x@yandex.ru')
        msg.body = 'Test message for me'
        mail.send(msg)
        print('Email sending!')
    except Exception as e:
        print(e)













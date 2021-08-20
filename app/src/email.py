import smtplib
import datetime
import time 

from flask_mail import Message
from app import application

from flask import render_template
from app.src.database import Patient, Record
from sqlalchemy import and_
from datetime import datetime as DT, timedelta


dt_fmt = '%d.%m.%Y'
now = datetime.datetime.now()
current_time = str(now.strftime('%H:%M:%S'))
current_date = str(now.strftime('%d.%m.%Y'))


def send_emails(asd):
    time.sleep(2)
    need_sending = False
    is_sending = False
    data = []
    for patient in Patient.query.filter(and_(Patient.email!= None, Patient.email.contains('@'))):
        for record in patient.records:
            obj_record_time = (DT.strptime(record.date, dt_fmt) - timedelta(days=3)).strftime(dt_fmt)
            if obj_record_time == current_date:
                # data.append([patient.full_name,record.date,record.time,\
                #         record.doctor.full_name, record.doctor.division, patient.email])

                server = smtplib.SMTP('smtp.yandex.com', 465)
                server.ehlo()
                server.starttls()
                server.login(application.config['YANDEX_MAIL'], application.config['YANDEX_PASS'])
                message = u"""
                Здравствуйте уважаемый {}!
                Обратите внимание у вас есть запись в клинике, на {} в {}
                к доктору {} {}, не опаздывайте к врачу, у врача плотный график!
                """.format(patient.full_name, record.date, record.time, record.doctor.full_name, record.doctor.division).encode('utf-8')
                server.sendmail(application.config['YANDEX_MAIL'], patient.email, message).encode('utf-8')
                server.quit()
                print(f"E-mails successfully sent! {patient.email}")
                time.sleep(2)
                break



import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid
from email.mime.text import MIMEText
import datetime
import time

from sqlalchemy import and_
from datetime import datetime as DT, timedelta


dt_fmt = '%d.%m.%Y'
now = datetime.datetime.now()
current_date = datetime.datetime.today().date()
date = datetime.date.today() + timedelta(days=3)
context = ssl.create_default_context()
# current_date = date.strftime('%d.%m.%Y')
print(current_date)

def send_emails():
    from app import mail, application, db
    from app.src.database import Record
    while True:
        for record in Record.query.filter(Record.is_send=='0'):
            obj_data = datetime.datetime.strptime(record.date, '%d.%m.%Y').date()
            if obj_data <= current_date + datetime.timedelta(days=3) and obj_data >= current_date:
                if record.patient_id and record.patient.email != None:
                    if '@yandex.ru' in record.patient.email:
                        SENDER = application.config['Y_MAIL_USERNAME']
                        PASSWORD = application.config['Y_MAIL_PASS']
                        SMTP = application.config['Y_MAIL_SERVER']
                        PORT = application.config['MAIL_PORT']
                    else:
                        SENDER = application.config['MAIL_USERNAME']
                        PASSWORD = application.config['MAIL_PASS']
                        SMTP = application.config['MAIL_SERVER']
                        PORT = application.config['Y_MAIL_PORT']
                    try:
                        msg = MIMEMultipart('alternative')
                        msg['Subject'] = "Оповещение"
                        msg['From'] = 'Med Site'
                        msg['To'] = record.patient.email
                        html = f'''
                        <html>
                        <body>
                        <p>Здравствуйте {record.patient.full_name}!</p>
                        Напоминаем, что {record.date} в {record.time} вы записаны к врачу {record.doctor.full_name}. Направление {record.doctor.division}.
                        Кабинет №{record.office}.

                        </body>
                        </html>
                        '''
                        part2 = MIMEText(html, 'html')
                        msg['Message-ID'] = make_msgid()
                        msg.add_header('Content-Type', 'text/html')
                        msg.attach(part2)
                        print(f"[+] Sending email to {record.patient.email} ")
                        server = smtplib.SMTP(SMTP, PORT)
                        server.starttls(context=context)
                        server.ehlo()
                        server.login(SENDER, PASSWORD)
                        server.sendmail(SENDER, record.patient.email, str(msg).encode('utf-8'))
                        server.quit()
                        record.is_send = True
                        db.session.commit()
                        print(f'[-] Email success sending [{record.patient.email}]')
                        time.sleep(3)
                        pass
                    except  Exception as e:
                        print(e)
                        print(f'[-] Email not sending [{record.patient.email}]')
        
        print('[-] Email end sending')
        time.sleep(3)
        break












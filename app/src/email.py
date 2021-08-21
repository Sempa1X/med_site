import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

from sqlalchemy import and_
from datetime import datetime as DT, timedelta




dt_fmt = '%d.%m.%Y'
date = datetime.date.today() + timedelta(days=3)
current_date = date.strftime('%d.%m.%Y')

def send_emails():
    from app import mail, application, db
    from app.src.database import Record
    for record in Record.query.filter(and_(Record.is_send==False, Record.date==current_date, Record.isActive==True)):
        print(f'Patient {record.patient.full_name}')
        if record.patient.email != None:
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

                msg.attach(part2)
                print(f"[+] Sending email to {record.patient.email} ")
                server = smtplib.SMTP_SSL('smtp.gmail.com')

                server.login('iazanov471@gmail.com', 'asdasdss228')
                server.sendmail('iazanov471@gmail.com', record.patient.email, str(msg).encode('utf-8'))
                server.quit()
                record.is_send = True
                db.session.commit()
            except  Exception as e:
                print(f'[-] Email not sending [{record.patient.email}]')
    print('[-] Email end sending')
    pass













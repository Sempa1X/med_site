import datetime
import os 

from app import application, db 
from docxtpl import DocxTemplate

now = datetime.datetime.now()
current_date = str(now.strftime('%d.%m.%Y'))

def create_doc():
    doc = DocxTemplate(os.path.abspath(os.path.dirname('app')) + "/app/static/documents/doc/base.docx")
    context = { 'patient_full_name' : 'Азанов Игорь Евгеньевич', 
                'age': '20 лет',
                'diagnoz': 'АУЕ мозга',
                'birthday': '18.07.2001',
                'osmotr': 'Еще жив',
                'end': 'Для жизни хватит',
                'desc': 'Описание',
                'doctor_full_name ': 'Test doctor 1'   }
    doc.render(context)
    path = os.path.abspath(os.path.dirname('app')) + f"/app/static/documents/created/{current_date}.docx"
    doc.save(os.path.abspath(os.path.dirname('app')) + f"/app/static/documents/created/{current_date}.docx")
    return path
import datetime
import os 

from app import application, db 
from docxtpl import DocxTemplate

now = datetime.datetime.now()
current_date = str(now.strftime('%d.%m.%Y'))

def create_doc():
    doc = DocxTemplate(os.path.abspath(os.path.dirname('app')) + "/app/static/documents/doc/base.docx")
    context = { 'test' : "И.И.Иванов"}
    doc.render(context)
    doc.save(os.path.abspath(os.path.dirname('app')) + f"/app/static/documents/created/{current_date}.docx")
    return current_date
import os
from datetime import datetime
from flask import Blueprint, render_template, send_file, request, redirect, url_for, flash

from app.src.document import create_doc
from app.src.database import Document, Patient
from app import application


bp_doc = Blueprint('doc', __name__, url_prefix='/doc')
now = datetime.now()
current_date = str(now.strftime('%d.%m.%Y'))


@bp_doc.route('/')
def index():
    docs = []
    patients = []
    for i in Document.query.filter(Document.date.endswith(current_date)):
        docs.append(i)
    for i in Patient.query.all():
        patients.append(i.full_name)
    return render_template('doc/doc.html', docs=docs, patients=patients)


@bp_doc.post('/sender')
def sender():
    path = create_doc(request.form['fio'], request.form['age'], request.form['diagnoz'],\
        request.form['birthday'], request.form['osmotr'], request.form['end'], request.form['desc'],\
        request.form['doctor_full_name'], request.form['apparate'], request.form['lp'], request.form['lp_full'],\
        request.form['lp_index'], request.form['lzd'], request.form['lzs'], request.form['lzd_index'],\
        request.form['vals'], request.form['sin'], request.form['vos'], request.form['duga'],\
        request.form['kdo'], request.form['kso'], request.form['kdo_index'], request.form['pp'],\
        request.form['pz'], request.form['npv'], request.form['mzp'], request.form['zs'],\
        request.form['imm'], request.form['la'], request.form['la_mm'], request.form['fb'],\
        request.form['fbt'], request.form['vmax'], request.form['pmax'], request.form['pmean'],\
        request.form['ava'], request.form['pegu'], request.form['vmaxMV'], request.form['pmaxMV'],\
        request.form['pmeanMV'], request.form['mva'], request.form['regu2'], request.form['vmaxPV'],\
        request.form['pmaxPV'], request.form['pmeanPV'], request.form['regu3'], request.form['vmaxTV'],\
        request.form['pmaxTV'], request.form['pmeanTV'], request.form['regu4'])
    if path == 'Не удалось сохранить файл':
        return redirect(url_for('doc.index'))
    else:
        filename = path.split('/')[-1]
        return send_file(path, attachment_filename=filename, as_attachment=True)


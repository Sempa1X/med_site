from io import BytesIO
import os
from flask import Blueprint, send_file, redirect, url_for

from app.src.document import create_doc
from app import application


bp_doc = Blueprint('doc', __name__, url_prefix='/doc')


@bp_doc.route('/')
def index():
    return redirect(url_for('doc.sender'))


@bp_doc.route('/sender')
def sender():
    filename = create_doc()
    path = os.path.abspath(os.path.dirname('app')) + f"app/static/documents/created/{filename}.docx"
    return send_file(path, attachment_filename=f'{filename}.docx', as_attachment=True)


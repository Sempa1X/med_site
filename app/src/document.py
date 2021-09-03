import datetime
import os 

from docxtpl import DocxTemplate

from app import application, db 
from app.src.database import Document, Result, Patient


now = datetime.datetime.now()
current_date = str(now.strftime('%d.%m.%Y'))


def create_doc(patient_full_name=None, age=None, diagnoz=None, \
    birthday=None, osmotr=None, end=None, desc=None, doctor_full_name=None,\
    apparate=None,lp=None, lp_full=None, lp_index=None, lzd=None, lzs=None,\
    lzd_index=None, vals=None, sin=None,vos=None, duga=None, kdo=None, kso=None,\
    kdo_index=None, pp=None, pz=None, npv=None, mzp=None, zs=None, imm=None, la=None,\
    la_mm=None, fb=None, fbt=None, vmax=None, pmax=None, pmean=None, ava=None, pegu=None,\
    vmaxMV=None, pmaxMV=None, pmeanMV=None, mva=None, regu2=None, vmaxPV=None, pmaxPV=None,\
    pmeanPV=None, regu3=None, vmaxTV=None, pmaxTV=None, pmeanTV=None, regu4=None
    ):
    
    doc = DocxTemplate(os.path.abspath(os.path.dirname('app')) + "/app/static/documents/doc/base.docx")
    context = { 'patient_full_name' : patient_full_name, 
                'age': age,
                'diagnoz': diagnoz,
                'birthday': birthday,
                'osmotr': osmotr,
                'end': end,
                'desc': desc,
                'doctor_full_name ': doctor_full_name,
                'apparate': apparate,
                'lp':lp, 
                'lp_full':lp_full,
                'lp_index': lp_index, 
                'lzd': lzd,
                'lzs': lzs,
                'lzd_index':lzd_index,
                'vals': vals,
                'sin': sin,
                'vos': vos,
                'duga': duga, 
                'kdo': kdo,
                'kso': kso,
                'kdo_index': kdo_index,
                'pp': pp, 
                'pz': pz,
                'npv': npv,
                'mzp': mzp,
                'zs': zs,
                'imm': imm,
                'la': la,
                'la_mm': la_mm,
                'fb': fb, 
                'fbt': fbt,
                'vmax': vmax,
                'pmax': pmax,
                'pmean': pmean,
                'ava': ava,
                'pegu': pegu,
                'vmaxMV': vmaxMV,
                'pmaxMV': pmaxMV,
                'pmeanMV': pmeanMV,
                'mva': mva,
                'regu2': regu2,
                'vmaxPV': vmaxPV, 
                'pmaxPV': pmaxPV, 
                'pmeanPV': pmeanPV, 
                'regu3': regu3,
                'vmaxTV': vmaxTV, 
                'pmaxTV': pmaxTV,
                'pmeanTV': pmeanTV, 
                'regu4': regu4
                }
    doc.render(context)
    base_path = os.path.abspath(os.path.dirname('app')) + f"/app/static/documents/created/"
    filename = f'{current_date}-{patient_full_name}.docx'
    path = base_path + filename
    
    try:
        doc.save(base_path + filename)
        document = Document(date=current_date, path=filename)
        db.session.add(document)
        db.session.commit()
        pat = Patient.query.filter_by(full_name=patient_full_name).first()

        res = Result(patient_full_name=patient_full_name,
        age = age,diagnoz = diagnoz,birthday = birthday,\
        osmotr = osmotr,end = end,desc = desc,doctor_full_name = doctor_full_name,\
        apparate = apparate,lp = lp,lp_full = lp_full,lp_index = lp_index,\
        lzd = lzd,lzs = lzs,lzd_index = lzd_index,vals = vals,sin = sin,\
        vos = vos,duga = duga,kdo = kdo,kso = kso,kdo_index = kdo_index,\
        pp = pp,pz = pz,npv = npv,mzp = mzp,zs = zs,imm = imm,la = la,\
        la_mm = la_mm,fb = fb,fbt = fbt,vmax = vmax,pmax = pmax,pmean = pmean,\
        ava = ava,regu = pegu,vmaxMV = vmaxMV,pmaxMV = pmaxMV,pmeanMV = pmeanMV,\
        mva = mva,regu2 = regu2,vmaxPV = vmaxPV,pmaxPV = pmaxPV,pmeanPV = pmeanPV,\
        regu3 = regu3,vmaxTV = vmaxTV,pmaxTV = pmaxTV,pmeanTV = pmeanTV,regu4 = regu4, patient_id=pat.id)

        db.session.add(res)
        db.session.commit()

        return path
    except Exception as e:
        print(e)
        return 'Не удалось сохранить файл'











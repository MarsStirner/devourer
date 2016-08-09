# coding: utf-8

from devourer.models import ErrandFileAttach
from devourer.models.misc import Person, Organisation
from devourer.systemwide import db
from hitsl_utils.wm_api import ApiException


def save_errand_intgr_file_attach(fmeta, attach_data):
    filemeta_id = fmeta.id
    errand_id = attach_data['errand_id']

    doctor_code = attach_data.get('doctor_code')
    if not doctor_code:
        raise ApiException(400, u'Не передан код врача `doctor_code`')
    hospital_code = attach_data.get('hospital_code')
    if not hospital_code:
        raise ApiException(400, u'Не передан код ЛПУ `hospital_code`')

    set_person_id = find_doctor(doctor_code, hospital_code).id
    efa = ErrandFileAttach(errand_id=errand_id, filemeta_id=filemeta_id,
                           setPerson_id=set_person_id)
    db.session.add(efa)
    db.session.commit()


def find_doctor(person_code, org_code):
    person = Person.query.join(Organisation).filter(
        Person.regionalCode == person_code,
        Person.deleted == 0,
        Organisation.TFOMSCode == org_code,
        Organisation.deleted == 0
    ).first()
    if not person:
        raise ApiException(
            404,
            u'Не найден врач по коду {0} и коду ЛПУ {1}'.format(person_code, org_code)
        )
    return person

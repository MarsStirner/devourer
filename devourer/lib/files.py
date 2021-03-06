# coding: utf-8

import os
import mimetypes
import uuid
import logging
import urllib

from flask import url_for

from devourer.models import FileMeta, ErrandFileAttach, ActionFileAttach, FileAttachType
from devourer.systemwide import app, db
from hitsl_utils.safe import safe_uuid


logger = logging.getLogger('simple')


class FileSaveException(Exception):
    pass


def save_new_file(file, file_info=None):
    if file_info is None:
        file_info = {}
    if file.filename == '':
        raise FileSaveException('no file')
    filename = file.filename
    f_name = file_info.get('name') or filename
    extension = get_file_extension(filename)
    mimetype, _ = mimetypes.guess_type(filename)
    note = file_info.get('note')
    f_uuid = uuid.uuid4()

    fmeta = FileMeta(name=f_name, extension=extension, mimetype=mimetype,
                     note=note, uuid=f_uuid, deleted=1)
    db.session.add(fmeta)
    db.session.commit()

    fullpath = get_full_file_path(f_uuid.hex)
    dirname = os.path.dirname(fullpath)
    try:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        file.save(fullpath)
    except (IOError, OSError), e:
        logger.exception(u'Save new file error `{0}`'.format(filename))
        db.session.delete(fmeta)
        db.session.commit()
        raise FileSaveException(unicode(e))
    else:
        fmeta.query.filter(FileMeta.id == fmeta.id).update({
            'deleted': 0,
        }, synchronize_session=False)
        db.session.commit()

    return fmeta


def get_file_extension(filename):
    return os.path.splitext(filename)[1][1:].strip().lower()


def get_full_file_path(uuid_hex):
    return os.path.join(app.config['FILE_STORAGE_PATH'], make_file_path(uuid_hex))


def make_file_path(uuid_hex):
    directory = '{0}/{1}'.format(uuid_hex[0:2], uuid_hex[2:4])
    filename = uuid_hex
    return os.path.join(directory, filename)


def get_file_info(uuid_hex):
    o_uuid = safe_uuid(uuid_hex)
    if o_uuid:
        fmeta = db.session.query(FileMeta).filter(
            FileMeta.uuid == o_uuid,
            FileMeta.deleted == 0
        ).first()
        if fmeta:
            fname = fmeta.name
            mime = fmeta.mimetype
            guessed_mime = mimetypes.guess_type(fname)[0]
            if guessed_mime != mime:
                ext = fmeta.extension
                if ext:
                    fname = u'{0}.{1}'.format(fname, ext)
            return {
                'name': fname,
                'path': make_file_path(uuid_hex),
                'mime': mime
            }


def save_file_attach(fmeta, attach_data):
    fa = create_file_attach(fmeta, attach_data)
    db.session.add(fa)
    db.session.commit()
    return fa


def create_file_attach(fmeta, attach_data):
    attach_type = attach_data.get('attach_type')
    if attach_type == FileAttachType.errand[0]:
        attach = create_errand_file_attach(fmeta, attach_data)
    elif attach_type == FileAttachType.action[0]:
        attach = create_action_file_attach(fmeta, attach_data)
    else:
        raise ValueError('unknown attach_type')
    return attach


def create_errand_file_attach(fmeta, attach_data):
    errand_id = attach_data['errand_id']
    set_person_id = attach_data['set_person_id']
    filemeta_id = fmeta.id
    efa = ErrandFileAttach(errand_id=errand_id, filemeta_id=filemeta_id,
                           setPerson_id=set_person_id)
    return efa


def create_action_file_attach(fmeta, attach_data):
    action_id = attach_data['action_id']
    set_person_id = attach_data['set_person_id']
    filemeta_id = fmeta.id
    efa = ActionFileAttach(action_id=action_id, filemeta_id=filemeta_id,
                           setPerson_id=set_person_id)
    return efa


def get_file_meta_list():
    fmetas = db.session.query(FileMeta).filter(FileMeta.deleted == 0).order_by(
        FileMeta.id.desc()).limit(20)
    return [
        represent_file_meta(fmeta)
        for fmeta in fmetas
    ]


def represent_file_meta(fmeta, attach=None):
    dc = {
        'id': fmeta.id,
        'name': fmeta.name,
        'mimetype': fmeta.mimetype,
        'note': fmeta.note,
        'url': make_file_url(fmeta),
    }
    if attach:
        dc['attach'] = attach
    return dc


def make_file_url(fmeta):
    if fmeta.uuid:
        return u'{0}{1}'.format(
            app.config['DEVOURER_URL'],
            url_for('.api_0_file_download', fileid=fmeta.uuid.hex)
            # url_for('serve_file', fileid=fmeta.uuid.hex)
        )


def make_filename_header(filename):
    # using rfc5987 for filename encoding in 'Content-Disposition' header
    # another possible choice is RFC 6266
    if isinstance(filename, unicode):
        filename = filename.encode('utf-8')
    return u"filename*=UTF-8''{0}".format(urllib.quote(filename))
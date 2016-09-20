# coding: utf-8

import datetime
from devourer.systemwide import db
from hitsl_utils.enum import Enum


class FileAttachType(Enum):
    errand = 1, u'Поручения'
    action = 2, u'Action'


class ErrandFileAttach(db.Model):
    __tablename__ = u'ErrandFileAttach'

    id = db.Column(db.Integer, primary_key=True)
    errand_id = db.Column(db.Integer, nullable=False)
    filemeta_id = db.Column(db.Integer, db.ForeignKey('FileMeta.id'), nullable=False)
    setPerson_id = db.Column(db.Integer, db.ForeignKey('Person.id'))
    attachDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    deleted = db.Column(db.SmallInteger, nullable=False, server_default="'0'")

    file_meta = db.relationship('FileMeta')
    set_person = db.relationship('Person')

    def __json__(self):
        return {
            'id': self.id,
            'errand_id': self.errand_id,
            'filemeta_id': self.filemeta_id,
            'set_person_id': self.setPerson_id,
            'attach_date': self.attachDate
        }


class ActionFileAttach(db.Model):
    __tablename__ = u'ActionFileAttach'

    id = db.Column(db.Integer, primary_key=True)
    action_id = db.Column(db.Integer, nullable=False)
    filemeta_id = db.Column(db.Integer, db.ForeignKey('FileMeta.id'), nullable=False)
    setPerson_id = db.Column(db.Integer, db.ForeignKey('Person.id'))
    attachDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    deleted = db.Column(db.SmallInteger, nullable=False, server_default="'0'")

    file_meta = db.relationship('FileMeta')
    set_person = db.relationship('Person')

    def __json__(self):
        return {
            'id': self.id,
            'action_id': self.action_id,
            'filemeta_id': self.filemeta_id,
            'set_person_id': self.setPerson_id,
            'attach_date': self.attachDate
        }
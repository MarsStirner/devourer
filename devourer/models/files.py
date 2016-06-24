# coding: utf-8

import datetime
from devourer.systemwide import db
from devourer.models.utils import UUIDColumn


class FileGroupDocument(db.Model):
    __tablename__ = u'FileGroupDocument'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(128))


class FileMeta(db.Model):
    __tablename__ = u'FileMeta'

    id = db.Column(db.Integer, primary_key=True)
    createDatetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    modifyDatetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    name = db.Column(db.Unicode(255), nullable=False)
    extension = db.Column(db.Unicode(32))
    mimetype = db.Column(db.String(128), nullable=False, default='')
    path = db.Column(db.Unicode(512))
    uuid = db.Column(UUIDColumn(), nullable=False)
    external_id = db.Column(db.Integer)
    filegroup_id = db.Column(db.Integer, db.ForeignKey('FileGroupDocument.id'))
    idx = db.Column(db.Integer, nullable=False, default='0')
    deleted = db.Column(db.SmallInteger, nullable=False, default='0')
    note = db.Column(db.Unicode(1024))

    filegroup = db.relationship('FileGroupDocument', backref='files')

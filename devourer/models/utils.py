# coding: utf-8

import uuid
from sqlalchemy import types


class UUIDColumn(types.TypeDecorator):
    impl = types.Binary

    def __init__(self):
        types.TypeDecorator.__init__(self, length=16)

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return value.bytes
        elif value and isinstance(value, basestring):
            return uuid.UUID(value).bytes
        elif value:
            raise ValueError('value %s is not a valid uuid.UUId' % value)
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return uuid.UUID(bytes=value)
        else:
            return None

    def is_mutable(self):
        return False

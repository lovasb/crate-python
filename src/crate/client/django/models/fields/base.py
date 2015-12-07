# -*- coding: utf-8 -*-
import datetime
import uuid

from dateutil.parser import parse
from django.db.models import Field as _DjangoField
from django.db.models import (
    BooleanField as _DjangoBooleanField,
    SmallIntegerField as _DjangoSmallIntegerField,
    TextField as _DjangoTextField,
    IntegerField as _DjangoIntegerField,
    BigIntegerField as _DjangoBigIntegerField,
    FloatField as _DjangoFloatField,
    IPAddressField as _DjangoIPField,
    DateTimeField as DjangoDatetimeField
)

from django.db import models


__all__ = [
    "BooleanField",
    "StringField",
    "ByteField",
    "ShortField",
    "IntegerField",
    "LongField",
    "FloatField",
    "DoubleField",
    "IPField",
]


class DateTimeField(DjangoDatetimeField):
    def from_db_value(self, value, expression, connection, context):
        if not value:
            return
        try:
            return datetime.datetime.utcfromtimestamp(value / 1e3)
        except TypeError:
            pass #TODO: logging

    def get_prep_value(self, value):
        if value is None:
            return value

        if isinstance(value, str):
            value = parse(value) ## TODO: django common date parsing

        return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ') ## TODO: date to string (with and without timezone)


class AutoField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = None
        super(AutoField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = models.Field.get_prep_value(self, value)
        if value is None:
            return None
        return str(value)

    def pre_save(self, model_instance, add):
        """
        Returns field's value just before saving.
        """
        value = getattr(model_instance, self.attname)
        if value is None:
            value = uuid.uuid4()
            setattr(model_instance, self.attname, value)
        return value


class Field(_DjangoField):

    def __init__(self, *args, **kwargs):
        self.fulltext_index = kwargs.pop("fulltext_index", None)
        self.analyzer = kwargs.pop("analyzer", None)
        super(Field, self).__init__(*args, **kwargs)

    def get_placeholder(self, idx, db):
        return '?'


class BooleanField(_DjangoBooleanField, Field):
    pass


class StringField(_DjangoTextField, Field):
    pass


class ByteField(_DjangoIntegerField, Field):
    pass


class ShortField(_DjangoSmallIntegerField, Field):
    pass


class IntegerField(_DjangoIntegerField, Field):
    pass


class LongField(_DjangoBigIntegerField, Field):
    pass


class FloatField(_DjangoFloatField, Field):
    pass


class DoubleField(_DjangoFloatField, Field):
    pass


class IPField(_DjangoIPField, Field):
    pass

# TODO: ObjectField, TimeStampField

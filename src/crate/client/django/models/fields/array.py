# -*- coding: utf-8 -*-
from django.db.models import Field, Transform
from django.db.models import lookups
from django.utils.translation import gettext_lazy as _


class ArrayField(Field):
    empty_strings_allowed = False
    description = _('Crate array type')
    default_error_messages = {
        'invalid': _("'%(value)s' value must be valid array."),
    }

    def __init__(self, base_field, **kwargs):
        self.base_field = base_field
        super(ArrayField, self).__init__(**kwargs)

    def db_type(self, connection):
        return 'array'

    def get_transform(self, name):
        return KeyTransformFactory(name)


class KeyTransform(Transform):

    def __init__(self, key_name, *args, **kwargs):
        super(KeyTransform, self).__init__(*args, **kwargs)
        self.key_name = key_name

    def as_sql(self, compiler, connection):
        key_transforms = [self.key_name]

        previous = self.lhs
        while isinstance(previous, KeyTransform):
            key_transforms.insert(0, previous.key_name)
            previous = previous.lhs

        lhs, params = compiler.compile(previous)

        transforms = ''
        for tr in key_transforms:
            transforms += "['%s']" % tr

        return "ANY(%s%s)" % (lhs, transforms), params


class KeyTransformFactory(object):

    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, *args, **kwargs):
        return KeyTransform(self.key_name, *args, **kwargs)


class CrateArrayCommonLookup(lookups.Lookup):
    operator = ''

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s %s %s' % (rhs, self.operator, lhs), params


@ArrayField.register_lookup
class StartswithLookup(CrateArrayCommonLookup, lookups.StartsWith):
    operator = 'LIKE'


@ArrayField.register_lookup
class StartswithLookup(CrateArrayCommonLookup, lookups.IStartsWith):
    operator = 'LIKE'


@ArrayField.register_lookup
class GreaterThanLookup(CrateArrayCommonLookup, lookups.GreaterThan):
    operator = '<'


@ArrayField.register_lookup
class GreaterThanOrEqualLookup(CrateArrayCommonLookup, lookups.GreaterThanOrEqual):
    operator = '<='

@ArrayField.register_lookup
class LessThanLookup(CrateArrayCommonLookup, lookups.LessThan):
    operator = '>'


@ArrayField.register_lookup
class LessThanOrEqualLookup(CrateArrayCommonLookup, lookups.LessThanOrEqual):
    operator = '>='

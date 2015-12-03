# -*- coding: utf-8 -*-
from django.db.models import Field, Transform
from django.utils.translation import gettext_lazy as _


class DictField(Field):
    empty_strings_allowed = False
    description = _('Crate object type')
    default_error_messages = {
        'invalid': _("'%(value)s' value must be valid dictionary."),
    }

    def db_type(self, connection):
        return 'object'

    def get_transform(self, name):
        transform = super(DictField, self).get_transform(name)
        if transform:
            return transform
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

        return "%s%s" % (lhs, transforms), params


class KeyTransformFactory(object):

    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, *args, **kwargs):
        return KeyTransform(self.key_name, *args, **kwargs)
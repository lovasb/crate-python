# -*- coding: utf-8 -*-
import re
from django.core.exceptions import FieldDoesNotExist
from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql import compiler
from django.db.models.sql.query import get_order_dir
from crate.client.django.models.fields import DictField
from crate.client.django.models.expressions import CrateOrderBy

FORMAT_QMARK_REGEX = re.compile(r'(?<!%)%s')


class SQLCompiler(compiler.SQLCompiler):
    def convert_query(self, query):
        return FORMAT_QMARK_REGEX.sub('?', query).replace('%%', '%')

    def find_ordering_name(self, name, opts, alias=None, default_order='ASC', already_seen=None):
        name, order = get_order_dir(name, default_order)
        pieces = name.split(LOOKUP_SEP)
        ## TODO: othermodel__joined_dictfield__subfield
        try:
            if isinstance(self.query.model._meta.get_field(pieces[0]), DictField):
                return [(CrateOrderBy(pieces, descending=order), False)]
        except FieldDoesNotExist: ## pk field
            pass

        return super().find_ordering_name(name, opts, alias, order, already_seen)

    def as_sql(self, *args, **kwargs):
        sql, params = super().as_sql(*args, **kwargs)
        return self.convert_query(sql), params


class SQLInsertCompiler(compiler.SQLInsertCompiler, SQLCompiler):
    def as_sql(self, *args, **kwargs):
        return (
            (self.convert_query(stmt), params) for stmt, params in super().as_sql(*args, **kwargs)
        )


class SQLDeleteCompiler(compiler.SQLDeleteCompiler, SQLCompiler):
    def as_sql(self, *args, **kwargs):
        sql, params = super().as_sql(*args, **kwargs)
        return self.convert_query(sql), params


class SQLUpdateCompiler(compiler.SQLUpdateCompiler, SQLCompiler):
    def as_sql(self, *args, **kwargs):
        sql, params = super().as_sql(*args, **kwargs)
        return self.convert_query(sql), params


class SQLAggregateCompiler(compiler.SQLAggregateCompiler, SQLCompiler):
    pass

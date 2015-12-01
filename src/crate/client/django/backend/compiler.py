# -*- coding: utf-8 -*-
import re
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import OrderBy

from django.db.models.sql import compiler
from django.db.models.sql.query import get_order_dir
from crate.client.django.models.fields import DictField

FORMAT_QMARK_REGEX = re.compile(r'(?<!%)%s')


class SQLCompiler(compiler.SQLCompiler):
    def convert_query(self, query):
        return FORMAT_QMARK_REGEX.sub('?', query).replace('%%', '%')

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

# -*- coding: utf-8 -*-
from django.db.backends.base.operations import BaseDatabaseOperations


class DatabaseOperations(BaseDatabaseOperations):

    compiler_module = "crate.client.django.backend.compiler"

    def cache_key_culling_sql(self):
        """not implemented"""
        return None

    def distinct_sql(self, fields):
        if fields:
            return 'DISTINCT (%s),' % ', '.join(fields)
        else:
            return 'DISTINCT'

    def drop_foreignkey_sql(self):
        """not supported"""
        return ''

    def drop_sequence_sql(self, table):
        """not supported"""
        return ''

    def for_update_sql(self, nowait=False):
        return ''

    def fulltext_search_sql(self, field_name):
        return 'match({}, %s)'.format(field_name)

    def quote_name(self, name):
        if name.startswith('"') and name.endswith('"'):
            return name # Quoting once is enough.
        return '"%s"' % name

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        return [
            'DELETE FROM {0}'.format(table) for table in tables
        ]

    def start_transaction_sql(self):
        return ''

    def end_transaction_sql(self, success=True):
        return ''

    def bulk_insert_sql(self, fields, num_values):
        items_sql = "(%s)" % ", ".join(["%s"] * len(fields))
        return "VALUES " + ", ".join([items_sql] * num_values)

    def return_insert_id(self):
        return "RETURNING %s", ()
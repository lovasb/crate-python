# -*- coding: utf-8 -*-
try:
    from crate import client as Database
except ImportError as exc:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured("Error loading crate module: %s" % exc)

from django.db.backends.base.base import BaseDatabaseWrapper

from .client import DatabaseClient
from .creation import DatabaseCreation
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .validation import DatabaseValidation


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = 'crate'
    operators = {
        'exact': '= %s',
        'iexact': '= %s',
        'contains': 'LIKE %s',
        'icontains': 'LIKE %s',
        'regex': '%s',
        'iregex': '%s',
        'gt': '> %s',
        'gte': '>= %s',
        'lt': '< %s',
        'lte': '<= %s',
        'startswith': 'LIKE %s',
        'endswith': 'LIKE %s',
        'istartswith': 'LIKE %s',
        'iendswith': 'LIKE %s',
    }

    Database = Database

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

        self.features = DatabaseFeatures(self)
        self.ops = DatabaseOperations(self)
        self.client = DatabaseClient(self)
        self.creation = DatabaseCreation(self)
        self.introspection = DatabaseIntrospection(self)
        self.validation = DatabaseValidation(self)

    ### CREATING CONNECTIONS AND CURSORS

    def get_connection_params(self):
        """Returns a dict of parameters suitable for get_new_connection."""
        """servers = self.settings_dict.get("SERVERS", ["localhost:4200"])
        timeout = self.settings_dict.get("TIMEOUT", None)
        return {
            "servers": servers,
            "timeout": timeout
        }"""
        kwargs = { }

        settings_dict = self.settings_dict
        if settings_dict['HOST']:
            kwargs['servers'] = ['http://' + settings_dict['HOST'] + ':' + settings_dict['PORT']]

        return kwargs

    def get_new_connection(self, conn_params):
        """Opens a connection to the database."""
        return Database.connect(**conn_params)

    def init_connection_state(self):
        """Initializes the database connection settings."""
        pass

    def create_cursor(self):
        """Creates a cursor. Assumes that a connection is established."""
        return self.connection.cursor()

    ### COMMIT
    def _commit(self):
        pass
        # TODO: refresh?
        # if self.connection is not None:
        #     with self.wrap_database_errors:
        #         self.connection.client.

    ### SAVEPOINT STUFF NOT SUPPORTED

    def _savepoint(self, sid):
        pass

    def _savepoint_rollback(self, sid):
        pass

    def _savepoint_commit(self, sid):
        pass

    def _savepoint_allowed(self):
        return False

    ### AUTOCOMMIT NOT SUPPORTED

    def _set_autocommit(self, autocommit):
        pass

    ### TEST IF CONNECTION IS USABLE

    def is_usable(self):
        """check if connection works"""
        try:
            self.connection.client._json_request("GET", "/")
        except:
            return False
        else:
            return True

# -*- coding: utf-8 -*-
from django.db.backends.base.client import BaseDatabaseClient


class DatabaseClient(BaseDatabaseClient):
    executable_name = 'crash'

    def runshell(self):
        """TODO: run shell"""
        pass
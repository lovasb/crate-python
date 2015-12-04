from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.models import NOT_PROVIDED


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    def skip_default(self, field):
        """
        Some backends don't accept default values for certain columns types
        (i.e. MySQL longtext and longblob).
        """
        return False

    def prepare_default(self, value):
        pass

    def effective_default(self, field):
        return str

    # Actions

    def create_model(self, model):
        pass

    def delete_model(self, model):
        pass

    def alter_unique_together(self, model, old_unique_together, new_unique_together):
        pass

    def alter_index_together(self, model, old_index_together, new_index_together):
        pass

    def alter_db_table(self, model, old_db_table, new_db_table):
        pass

    def alter_db_tablespace(self, model, old_db_tablespace, new_db_tablespace):
        pass

    def add_field(self, model, field):
        pass

    def remove_field(self, model, field):
        pass

    def alter_field(self, model, old_field, new_field, strict=False):
        pass

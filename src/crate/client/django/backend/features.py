from django.db.backends.base.features import BaseDatabaseFeatures


class DatabaseFeatures(BaseDatabaseFeatures):
    # Does the backend distinguish between '' and None?
    interprets_empty_strings_as_nulls = False

    allows_group_by_pk = True
    # True if django.db.backend.utils.typecast_timestamp is used on values
    # returned from dates() calls.
    needs_datetime_string_cast = False
    update_can_self_select = True

    can_use_chunked_reads = False
    can_return_id_from_insert = False
    has_bulk_insert = True
    uses_savepoints = False
    can_combine_inserts_with_and_without_auto_increment_pk = False

    # If True, don't use integer foreign keys referring to, e.g., positive
    # integer primary keys.
    related_fields_match_type = False
    allow_sliced_subqueries = False
    has_select_for_update = False
    has_select_for_update_nowait = False

    supports_select_related = False

    # Does the default test database allow multiple connections?
    # Usually an indication that the test database is in-memory
    test_db_allows_multiple_connections = True

    # Can an object be saved without an explicit primary key?
    supports_unspecified_pk = False

    # Can a fixture contain forward references? i.e., are
    # FK constraints checked at the end of transaction, or
    # at the end of each save operation?
    supports_forward_references = False

    # Does a dirty transaction need to be rolled back
    # before the cursor can be used again?
    requires_rollback_on_dirty_transaction = False

    # Does the backend allow very long model names without error?
    supports_long_model_names = True

    # Is there a REAL datatype in addition to floats/doubles?
    has_real_datatype = False
    supports_subqueries_in_group_by = False
    supports_bitwise_or = False

    # Do time/datetime fields have microsecond precision?
    supports_microsecond_precision = True

    # Does the __regex lookup support backreferencing and grouping?
    supports_regex_backreferencing = False

    # Can date/datetime lookups be performed using a string?
    supports_date_lookup_using_string = True

    # Can datetimes with timezones be used?
    supports_timezones = False

    # Does the database have a copy of the zoneinfo database?
    has_zoneinfo_database = False

    # When performing a GROUP BY, is an ORDER BY NULL required
    # to remove any ordering?
    requires_explicit_null_ordering_when_grouping = False

    # Can an object have a primary key of 0? MySQL says No.
    allows_primary_key_0 = True

    # Do we need to NULL a ForeignKey out, or can the constraint check be
    # deferred
    can_defer_constraint_checks = False

    # date_interval_sql can properly handle mixed Date/DateTime fields and timedeltas
    supports_mixed_date_datetime_comparisons = True

    # Does the backend support tablespaces? Default to False because it isn't
    # in the SQL standard.
    supports_tablespaces = False

    # Does the backend reset sequences between tests?
    supports_sequence_reset = False

    # Confirm support for introspected foreign keys
    # Every database can do this reliably, except MySQL,
    # which can't do it for MyISAM tables
    can_introspect_foreign_keys = False

    # Support for the DISTINCT ON clause
    can_distinct_on_fields = True

    # Does the backend decide to commit before SAVEPOINT statements
    # when autocommit is disabled? http://bugs.python.org/issue8145#msg109965
    autocommits_when_autocommit_is_off = False

    # Does the backend prevent running SQL queries in broken transactions?
    atomic_transactions = False

    # Does the backend support 'pyformat' style ("... %(name)s ...", {'name': value})
    # parameter passing? Note this can be provided by the backend even if not
    # supported by the Python driver
    supports_paramstyle_pyformat = False
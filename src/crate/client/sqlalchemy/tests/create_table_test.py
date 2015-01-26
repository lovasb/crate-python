

from mock import patch, MagicMock
from unittest import TestCase

import sqlalchemy as sa
import sqlalchemy.types as types
from sqlalchemy.ext.declarative import declarative_base

from crate.client.cursor import Cursor


fake_cursor = MagicMock(name='fake_cursor')
FakeCursor = MagicMock(name='FakeCursor', spec=Cursor)
FakeCursor.return_value = fake_cursor


@patch('crate.client.connection.Cursor', FakeCursor)
class CreateTableTest(TestCase):

    def setUp(self):
        self.engine = sa.create_engine('crate://')
        self.Base = declarative_base(bind=self.engine)

        class Detail(types.UserDefinedType):
            age = sa.Column(sa.Integer)
            gender = sa.Column(sa.String)

            def get_col_spec(self):
                attributes = []
                for a in dir(self):
                    if a.startswith('_'):
                        continue
                    try:
                        attributes.append((a, getattr(self, a)))
                    except NotImplementedError:
                        pass
                columns = (c for c in attributes if isinstance(c[1], sa.Column))
                columns = ('{0} {1}'.format(c[0], c[1].type.compile()) for c in columns)
                columns = ', '.join(columns)
                return 'object as ({0})'.format(columns)


        class User(self.Base):
            __tablename__ = 'users'
            string_col = sa.Column(sa.String, primary_key=True)
            unicode_col = sa.Column(sa.Unicode)
            int_col = sa.Column(sa.Integer)
            long_col = sa.Column(sa.BigInteger)
            bool_col = sa.Column(sa.Boolean)
            short_col = sa.Column(sa.SmallInteger)
            ts_col = sa.Column(sa.DateTime)
            float_col = sa.Column(sa.Float)
            obj_col = sa.Column(Detail())


    def test_create_table(self):
        self.Base.metadata.create_all()
        fake_cursor.execute.assert_called_with(
            ('\nCREATE TABLE users (\n\tstring_col string, '
             '\n\tunicode_col string, \n\tint_col INTEGER, '
             '\n\tlong_col long, \n\tbool_col BOOLEAN, '
             '\n\tshort_col short, \n\tts_col timestamp, '
             '\n\tfloat_col FLOAT, \n\tPRIMARY KEY (string_col)\n)\n\n'
            ),
            ()
        )


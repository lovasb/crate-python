from django.db.models import Expression


class CrateOrderBy(Expression):

    def __init__(self, expression, descending=False):
        self.expression = expression
        self.descending = descending

    def as_sql(self, compiler, connection):
        retval = self.expression[0]
        for f in self.expression[1:]:
            retval += "['%s']" % f

        retval += ' DESC' if self.descending else ' ASC'
        return retval, ''

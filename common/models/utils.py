from django.db.models.fields import Field
from django.db import models


class NotEqual(models.Lookup):
    """A `not equal` query lookup."""

    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        """Return SQL representation."""
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return f"{lhs} <> {rhs}", params

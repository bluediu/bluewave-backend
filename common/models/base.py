from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.timezone import now


class BaseModel(models.Model):
    """Base model for project apps models."""

    created_at = models.DateTimeField(
        verbose_name="Creado",
        editable=False,
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Creado por",
        related_name="%(app_label)s_%(class)s_created_by",
        related_query_name="%(app_label)s_%(class)s_created_by",
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="Actualizado",
        editable=False,
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Actualizado por",
        related_name="%(app_label)s_%(class)s_updated_by",
        related_query_name="%(app_label)s_%(class)s_updated_by",
        editable=False,
    )

    AUDIT_FIELDS = {"created_by_id", "created_at", "updated_by_id", "updated_at"}

    class Meta:
        abstract = True
        default_permissions = ()

    def save(
        self,
        user_id=None,
        *,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        """Customize to set audit fields before saving."""
        current_timestamp = now()
        if self.pk is None:
            self.created_at = current_timestamp
            self.created_by_id = user_id
        self.updated_at = current_timestamp
        self.updated_by_id = user_id

        if update_fields is not None:
            update_fields = self.AUDIT_FIELDS.union(update_fields)

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def full_clean(
        self,
        *,
        include=None,
        exclude=None,
        validate_unique=True,
        validate_constraints=True,
    ):
        """
        Extend to exclude audit fields from cleaning.

        Required because there may be the case where audit
        fields are not set yet.
        """
        if include is not None:
            if exclude is not None:
                message = "`exclude` and `include` are mutually exclusive."
                raise ImproperlyConfigured(message)

            include = set(include)
            fields = {field.name for field in self._meta.get_fields()}
            exclude = fields.difference(include)

        exclude = self.AUDIT_FIELDS.union(exclude or {})

        super().full_clean(
            exclude=exclude,
            validate_unique=validate_unique,
            validate_constraints=validate_constraints,
        )

    def update_fields(self, **fields) -> list[str]:
        """Return a list of the changed fields."""
        changed_fields = []
        for field, value in fields.items():
            if getattr(self, field) != value:
                setattr(self, field, value)
                changed_fields.append(field)
        return changed_fields

    @property
    def is_new(self) -> bool:
        """Return True if the instance is being created."""
        return self.pk is None

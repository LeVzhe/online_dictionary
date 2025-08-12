from django.db import models


class BaseDjangoModel(models.Model):
    """
    Basic class for models.
    """

    created_at = models.DateTimeField(
        verbose_name="created_at",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="updated_at",
        auto_now=True,
    )

    def update_fields(self, *, should_save=True, **kwargs):
        """
        Update model fields
        """
        updated_fields = []
        for key, value in kwargs.items():
            if hasattr(self, key):
                field = getattr(self, key)
                if field != value:
                    updated_fields.append(key)
                    setattr(self, key, value)
        for field in self.__class__._meta.get_fields():
            if hasattr(field, "auto_now") and field.auto_now:
                updated_fields.append(field.name)
        if should_save:
            self.save(update_fields=updated_fields)

    class Meta:
        abstract = True


class BaseDataModel(BaseDjangoModel):
    """
    Basic class for data models.
    """

    is_archived = models.BooleanField(
        verbose_name="is archived",
        default=False,
    )

    class Meta:
        abstract = True

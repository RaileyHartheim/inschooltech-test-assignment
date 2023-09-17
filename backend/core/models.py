import uuid
from django.db import models


class SoftDeletionModel(models.Model):
    """ Base model which allows to soft delete its objects. """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="id"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created at"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="updated at"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="is active"
    )

    def delete(self):
        self.is_active = False
        self.save()

    class Meta:
        abstract = True

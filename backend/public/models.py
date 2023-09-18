from django.db import models

from core.models import SoftDeletionModel


class Lab(SoftDeletionModel):
    name = models.CharField(
        max_length=255,
        verbose_name="laboratory's name"
    )

    class Meta:
        verbose_name = "lab"
        verbose_name_plural = "labs"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class Test(SoftDeletionModel):
    started_at = models.DateTimeField(
        verbose_name="test started at",
        blank=True,
        null=True
    )
    completed_at = models.DateTimeField(
        verbose_name="test completed at",
        blank=True,
        null=True
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="comment for test"
    )
    lab_id = models.ForeignKey(
        Lab,
        on_delete=models.PROTECT,
        verbose_name="lab where test was taken"
    )

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "tests"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"test: {self.id}"

from django.db import models

from core.models import SoftDeletionModel
from public.models import Test


class Indicator(SoftDeletionModel):
    name = models.CharField(
        max_length=255,
        verbose_name="indicator's name"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="indicator's description"
    )

    class Meta:
        verbose_name = "indicators"
        verbose_name_plural = "indicators"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Metric(SoftDeletionModel):
    name = models.CharField(
        max_length=255,
        verbose_name="metric's name"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="metric's description"
    )
    unit = models.CharField(
        max_length=255,
        verbose_name="metric's unit"
    )

    class Meta:
        verbose_name = "metric"
        verbose_name_plural = "metrics"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class IndicatorMetric(SoftDeletionModel):
    indicator_id = models.ForeignKey(
        Indicator,
        on_delete=models.PROTECT
    )
    metric_id = models.ForeignKey(
        Metric,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "indicator - metric pair"
        verbose_name_plural = "indicator - metric pairs"

    def __str__(self) -> str:
        return f"indicator: {self.indicator_id.name}, metric: {self.metric_id.name}"


class Score(SoftDeletionModel):
    score = models.DecimalField(
        verbose_name="score",
        max_digits=20,
        decimal_places=10
    )
    test_id = models.ForeignKey(
        Test,
        on_delete=models.PROTECT,
        related_name="scores"
    )
    indicator_metric_id = models.ForeignKey(
        IndicatorMetric,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "score"
        verbose_name_plural = "scores"
        unique_together = ("indicator_metric_id", "test_id",)

    def __str__(self) -> str:
        return f"score for test {self.test_id}"


class Reference(SoftDeletionModel):
    min_score = models.DecimalField(
        verbose_name="minimal score",
        max_digits=20,
        decimal_places=10
    )
    max_score = models.DecimalField(
        verbose_name="maximal score",
        max_digits=20,
        decimal_places=10
    )
    indicator_metric_id = models.ForeignKey(
        IndicatorMetric,
        on_delete=models.PROTECT,
        unique=True
    )

    class Meta:
        verbose_name = "reference"
        verbose_name_plural = "references"

    def __str__(self) -> str:
        return f"reference for indicator-metric pair {self.indicator_metric_id}"

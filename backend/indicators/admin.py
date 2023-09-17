from django.contrib import admin

from .models import Indicator, IndicatorMetric, Metric, Reference, Score


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "created_at",
        "updated_at",
        "is_active",
    )
    empty_value_display = "-empty-"


@admin.register(IndicatorMetric)
class IndicatorMetricAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "indicator_id",
        "metric_id",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_select_related = ("indicator_id", "metric_id",)
    empty_value_display = "-empty-"


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "unit",
        "created_at",
        "updated_at",
        "is_active",
    )
    empty_value_display = "-empty-"


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "min_score",
        "max_score",
        "indicator_metric_id",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_select_related = (
        "indicator_metric_id",
        "indicator_metric_id__indicator_id",
        "indicator_metric_id__metric_id",
    )
    empty_value_display = "-empty-"


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "test_id",
        "indicator_metric_id",
        "score",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_select_related = (
        "test_id",
        "indicator_metric_id",
        "indicator_metric_id__indicator_id",
        "indicator_metric_id__metric_id",
    )
    empty_value_display = "-empty-"

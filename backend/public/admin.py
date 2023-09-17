from django.contrib import admin

from .models import Lab, Test


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
        "updated_at",
        "is_active",
        )
    empty_value_display = "-empty-"


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "lab_id",
        "started_at",
        "completed_at",
        "comment",
        "is_active",
    )
    list_select_related = (
        "lab_id",
    )
    empty_value_display = "-empty-"

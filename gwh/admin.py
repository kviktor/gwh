from django.contrib import admin

from .models import MetricConfig


@admin.register(MetricConfig)
class MetricConfigAdmin(admin.ModelAdmin):
    pass

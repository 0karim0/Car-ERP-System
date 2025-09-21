"""
Admin configuration for reports app.
"""
from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Report admin interface.
    """
    list_display = ['name', 'report_type', 'format', 'is_generated', 'generation_status', 'created_at', 'created_by']
    list_filter = ['report_type', 'format', 'is_generated', 'generation_status', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['generation_status']
    readonly_fields = ['created_at', 'generated_at']
    raw_id_fields = ['created_by']
    date_hierarchy = 'created_at'

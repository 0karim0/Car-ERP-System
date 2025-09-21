"""
Admin configuration for job_orders app.
"""
from django.contrib import admin
from .models import (
    JobOrder, JobOrderItem, TechnicianTime, JobOrderPhoto, JobOrderStatusHistory
)


@admin.register(JobOrder)
class JobOrderAdmin(admin.ModelAdmin):
    """
    Job Order admin interface.
    """
    list_display = ['job_number', 'customer', 'vehicle', 'service_type', 'status', 'priority', 'received_date']
    list_filter = ['status', 'priority', 'received_date', 'assigned_technician']
    search_fields = ['job_number', 'customer__first_name', 'customer__last_name', 'vehicle__license_plate', 'service_type']
    list_editable = ['status', 'priority']
    readonly_fields = ['job_number', 'received_date', 'updated_at']
    raw_id_fields = ['customer', 'vehicle', 'assigned_technician', 'created_by']
    date_hierarchy = 'received_date'
    
    fieldsets = (
        ('Job Information', {
            'fields': ('job_number', 'customer', 'vehicle', 'service_type', 'description')
        }),
        ('Customer Information', {
            'fields': ('customer_complaint',)
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'assigned_technician')
        }),
        ('Dates', {
            'fields': ('received_date', 'estimated_completion', 'actual_completion')
        }),
        ('Financial', {
            'fields': ('estimated_cost', 'actual_cost')
        }),
        ('Notes', {
            'fields': ('notes', 'internal_notes')
        }),
        ('System Information', {
            'fields': ('created_by', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(JobOrderItem)
class JobOrderItemAdmin(admin.ModelAdmin):
    """
    Job Order Item admin interface.
    """
    list_display = ['job_order', 'name', 'item_type', 'quantity', 'unit_price', 'total_price']
    list_filter = ['item_type', 'job_order__status']
    search_fields = ['job_order__job_number', 'name', 'description']
    raw_id_fields = ['job_order']


@admin.register(TechnicianTime)
class TechnicianTimeAdmin(admin.ModelAdmin):
    """
    Technician Time admin interface.
    """
    list_display = ['job_order', 'technician', 'start_time', 'end_time', 'hours_worked']
    list_filter = ['start_time', 'technician']
    search_fields = ['job_order__job_number', 'technician__first_name', 'technician__last_name']
    raw_id_fields = ['job_order', 'technician']
    readonly_fields = ['hours_worked', 'created_at', 'updated_at']


@admin.register(JobOrderPhoto)
class JobOrderPhotoAdmin(admin.ModelAdmin):
    """
    Job Order Photo admin interface.
    """
    list_display = ['job_order', 'photo_type', 'title', 'taken_at', 'taken_by']
    list_filter = ['photo_type', 'taken_at']
    search_fields = ['job_order__job_number', 'title', 'description']
    raw_id_fields = ['job_order', 'taken_by']
    readonly_fields = ['taken_at']


@admin.register(JobOrderStatusHistory)
class JobOrderStatusHistoryAdmin(admin.ModelAdmin):
    """
    Job Order Status History admin interface.
    """
    list_display = ['job_order', 'old_status', 'new_status', 'changed_at', 'changed_by']
    list_filter = ['old_status', 'new_status', 'changed_at']
    search_fields = ['job_order__job_number', 'notes']
    raw_id_fields = ['job_order', 'changed_by']
    readonly_fields = ['changed_at']
    date_hierarchy = 'changed_at'

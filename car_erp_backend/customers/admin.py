"""
Admin configuration for customers app.
"""
from django.contrib import admin
from .models import Customer, CustomerDocument, CustomerCommunication, Appointment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Customer admin interface.
    """
    list_display = ['full_name', 'email', 'phone', 'city', 'is_active', 'created_at']
    list_filter = ['is_active', 'city', 'state', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'company_name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'alternate_phone', 'gender', 'date_of_birth')
        }),
        ('Address Information', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Business Information', {
            'fields': ('company_name', 'tax_id')
        }),
        ('Additional Information', {
            'fields': ('notes', 'preferred_contact_method', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    """
    Customer Document admin interface.
    """
    list_display = ['customer', 'document_type', 'title', 'uploaded_at', 'uploaded_by']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'title']
    raw_id_fields = ['customer', 'uploaded_by']
    readonly_fields = ['uploaded_at']


@admin.register(CustomerCommunication)
class CustomerCommunicationAdmin(admin.ModelAdmin):
    """
    Customer Communication admin interface.
    """
    list_display = ['customer', 'communication_type', 'direction', 'subject', 'communication_date', 'created_by']
    list_filter = ['communication_type', 'direction', 'communication_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'subject', 'message']
    raw_id_fields = ['customer', 'created_by']
    readonly_fields = ['communication_date']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Appointment admin interface.
    """
    list_display = ['customer', 'appointment_date', 'service_type', 'status', 'assigned_to', 'created_by']
    list_filter = ['status', 'appointment_date', 'service_type']
    search_fields = ['customer__first_name', 'customer__last_name', 'service_type', 'description']
    raw_id_fields = ['customer', 'created_by', 'assigned_to']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'appointment_date'


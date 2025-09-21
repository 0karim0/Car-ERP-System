"""
Admin configuration for vehicles app.
"""
from django.contrib import admin
from .models import Vehicle, VehicleDocument, VehiclePhoto, VehicleHistory


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Vehicle admin interface.
    """
    list_display = ['full_description', 'customer', 'year', 'fuel_type', 'is_active', 'created_at']
    list_filter = ['make', 'model', 'year', 'fuel_type', 'is_active', 'created_at']
    search_fields = ['make', 'model', 'license_plate', 'vin', 'customer__first_name', 'customer__last_name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['customer', 'created_by']
    
    fieldsets = (
        ('Vehicle Information', {
            'fields': ('make', 'model', 'year', 'vin', 'license_plate', 'color')
        }),
        ('Specifications', {
            'fields': ('engine_size', 'fuel_type', 'transmission', 'mileage', 'engine_number')
        }),
        ('Ownership', {
            'fields': ('customer', 'registration_date', 'insurance_expiry')
        }),
        ('Additional Information', {
            'fields': ('notes', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VehicleDocument)
class VehicleDocumentAdmin(admin.ModelAdmin):
    """
    Vehicle Document admin interface.
    """
    list_display = ['vehicle', 'document_type', 'title', 'expiry_date', 'uploaded_at', 'uploaded_by']
    list_filter = ['document_type', 'uploaded_at', 'expiry_date']
    search_fields = ['vehicle__make', 'vehicle__model', 'vehicle__license_plate', 'title']
    raw_id_fields = ['vehicle', 'uploaded_by']
    readonly_fields = ['uploaded_at']


@admin.register(VehiclePhoto)
class VehiclePhotoAdmin(admin.ModelAdmin):
    """
    Vehicle Photo admin interface.
    """
    list_display = ['vehicle', 'photo_type', 'title', 'taken_at', 'taken_by']
    list_filter = ['photo_type', 'taken_at']
    search_fields = ['vehicle__make', 'vehicle__model', 'vehicle__license_plate', 'title']
    raw_id_fields = ['vehicle', 'taken_by']
    readonly_fields = ['taken_at']


@admin.register(VehicleHistory)
class VehicleHistoryAdmin(admin.ModelAdmin):
    """
    Vehicle History admin interface.
    """
    list_display = ['vehicle', 'service_date', 'service_type', 'mileage_at_service', 'cost', 'created_by']
    list_filter = ['service_type', 'service_date']
    search_fields = ['vehicle__make', 'vehicle__model', 'vehicle__license_plate', 'service_type', 'description']
    raw_id_fields = ['vehicle', 'created_by']
    readonly_fields = ['created_at']
    date_hierarchy = 'service_date'

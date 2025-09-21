"""
Admin configuration for inventory app.
"""
from django.contrib import admin
from .models import (
    Category, Supplier, Part, PartPhoto, PurchaseOrder, 
    PurchaseOrderItem, StockMovement
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category admin interface.
    """
    list_display = ['name', 'description', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Supplier admin interface.
    """
    list_display = ['name', 'contact_person', 'email', 'phone', 'city', 'is_active', 'created_at']
    list_filter = ['is_active', 'city', 'state', 'created_at']
    search_fields = ['name', 'contact_person', 'email', 'phone']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['created_by']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'contact_person', 'email', 'phone', 'fax')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Business Information', {
            'fields': ('tax_id', 'website', 'payment_terms', 'credit_limit')
        }),
        ('Additional Information', {
            'fields': ('notes', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    """
    Part admin interface.
    """
    list_display = ['sku', 'name', 'brand', 'category', 'supplier', 'current_stock', 'is_active']
    list_filter = ['category', 'supplier', 'brand', 'is_active', 'is_low_stock']
    search_fields = ['sku', 'name', 'brand', 'model', 'part_number']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at', 'is_low_stock', 'needs_reorder']
    raw_id_fields = ['category', 'supplier', 'created_by']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('sku', 'name', 'description', 'brand', 'model', 'part_number')
        }),
        ('Category & Supplier', {
            'fields': ('category', 'supplier')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price')
        }),
        ('Inventory', {
            'fields': ('current_stock', 'minimum_stock', 'maximum_stock', 'reorder_point', 'reorder_quantity', 'unit')
        }),
        ('Additional Information', {
            'fields': ('location', 'notes', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PartPhoto)
class PartPhotoAdmin(admin.ModelAdmin):
    """
    Part Photo admin interface.
    """
    list_display = ['part', 'title', 'uploaded_at', 'uploaded_by']
    list_filter = ['uploaded_at']
    search_fields = ['part__name', 'title', 'description']
    raw_id_fields = ['part', 'uploaded_by']
    readonly_fields = ['uploaded_at']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    """
    Purchase Order admin interface.
    """
    list_display = ['po_number', 'supplier', 'status', 'total_amount', 'order_date', 'created_by']
    list_filter = ['status', 'order_date', 'supplier']
    search_fields = ['po_number', 'supplier__name']
    list_editable = ['status']
    readonly_fields = ['po_number', 'order_date', 'updated_at']
    raw_id_fields = ['supplier', 'created_by']
    date_hierarchy = 'order_date'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('po_number', 'supplier', 'status')
        }),
        ('Dates', {
            'fields': ('order_date', 'expected_delivery', 'actual_delivery')
        }),
        ('Financial', {
            'fields': ('subtotal', 'tax_amount', 'shipping_cost', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes', 'terms_conditions')
        }),
        ('System Information', {
            'fields': ('created_by', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    """
    Purchase Order Item admin interface.
    """
    list_display = ['purchase_order', 'part', 'quantity_ordered', 'quantity_received', 'unit_cost', 'total_cost']
    list_filter = ['purchase_order__status']
    search_fields = ['purchase_order__po_number', 'part__name']
    raw_id_fields = ['purchase_order', 'part']
    readonly_fields = ['created_at', 'updated_at', 'total_cost']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    """
    Stock Movement admin interface.
    """
    list_display = ['part', 'movement_type', 'quantity', 'previous_stock', 'new_stock', 'created_at', 'created_by']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['part__name', 'notes']
    raw_id_fields = ['part', 'created_by']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

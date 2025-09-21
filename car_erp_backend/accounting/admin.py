"""
Admin configuration for accounting app.
"""
from django.contrib import admin
from .models import (
    Invoice, InvoiceItem, Payment, SupplierPayment, Expense,
    AccountReceivable, AccountPayable
)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Invoice admin interface.
    """
    list_display = ['invoice_number', 'customer', 'job_order', 'status', 'total_amount', 'invoice_date', 'due_date']
    list_filter = ['status', 'payment_terms', 'invoice_date', 'due_date']
    search_fields = ['invoice_number', 'customer__first_name', 'customer__last_name', 'job_order__job_number']
    list_editable = ['status']
    readonly_fields = ['invoice_number', 'invoice_date', 'updated_at', 'balance_due']
    raw_id_fields = ['customer', 'job_order', 'created_by']
    date_hierarchy = 'invoice_date'
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'customer', 'job_order', 'status', 'payment_terms')
        }),
        ('Dates', {
            'fields': ('invoice_date', 'due_date', 'paid_date')
        }),
        ('Financial', {
            'fields': ('subtotal', 'tax_rate', 'tax_amount', 'discount_amount', 'total_amount', 'paid_amount', 'balance_due')
        }),
        ('Additional Information', {
            'fields': ('notes', 'terms_conditions')
        }),
        ('System Information', {
            'fields': ('created_by', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    """
    Invoice Item admin interface.
    """
    list_display = ['invoice', 'description', 'quantity', 'unit_price', 'total_price']
    list_filter = ['invoice__status']
    search_fields = ['invoice__invoice_number', 'description']
    raw_id_fields = ['invoice']
    readonly_fields = ['created_at', 'total_price']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Payment admin interface.
    """
    list_display = ['payment_number', 'customer', 'invoice', 'amount', 'payment_method', 'status', 'payment_date']
    list_filter = ['payment_method', 'status', 'payment_date']
    search_fields = ['payment_number', 'customer__first_name', 'customer__last_name', 'invoice__invoice_number']
    list_editable = ['status']
    readonly_fields = ['payment_number', 'payment_date']
    raw_id_fields = ['customer', 'invoice', 'created_by', 'processed_by']
    date_hierarchy = 'payment_date'


@admin.register(SupplierPayment)
class SupplierPaymentAdmin(admin.ModelAdmin):
    """
    Supplier Payment admin interface.
    """
    list_display = ['payment_number', 'supplier', 'purchase_order', 'amount', 'payment_method', 'status', 'payment_date']
    list_filter = ['payment_method', 'status', 'payment_date']
    search_fields = ['payment_number', 'supplier__name', 'purchase_order__po_number']
    list_editable = ['status']
    readonly_fields = ['payment_number', 'payment_date']
    raw_id_fields = ['supplier', 'purchase_order', 'created_by', 'processed_by']
    date_hierarchy = 'payment_date'


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """
    Expense admin interface.
    """
    list_display = ['expense_number', 'category', 'description', 'amount', 'status', 'expense_date', 'created_by']
    list_filter = ['category', 'status', 'expense_date']
    search_fields = ['expense_number', 'description', 'notes']
    list_editable = ['status']
    readonly_fields = ['expense_number', 'expense_date']
    raw_id_fields = ['created_by', 'approved_by']
    date_hierarchy = 'expense_date'


@admin.register(AccountReceivable)
class AccountReceivableAdmin(admin.ModelAdmin):
    """
    Account Receivable admin interface.
    """
    list_display = ['customer', 'invoice', 'original_amount', 'current_amount', 'due_date']
    list_filter = ['due_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'invoice__invoice_number']
    raw_id_fields = ['customer', 'invoice']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'


@admin.register(AccountPayable)
class AccountPayableAdmin(admin.ModelAdmin):
    """
    Account Payable admin interface.
    """
    list_display = ['supplier', 'purchase_order', 'original_amount', 'current_amount', 'due_date']
    list_filter = ['due_date']
    search_fields = ['supplier__name', 'purchase_order__po_number']
    raw_id_fields = ['supplier', 'purchase_order']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'

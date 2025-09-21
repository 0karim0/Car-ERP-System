"""
Accounting serializers for Car ERP System.
"""
from rest_framework import serializers
from .models import (
    Invoice, InvoiceItem, Payment, SupplierPayment, Expense,
    AccountReceivable, AccountPayable
)
from customers.serializers import CustomerSerializer
from job_orders.serializers import JobOrderSerializer
from inventory.serializers import SupplierSerializer, PurchaseOrderSerializer
from authentication.serializers import UserSerializer


class InvoiceItemSerializer(serializers.ModelSerializer):
    """
    Invoice Item serializer.
    """
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ['created_at', 'total_price']


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Invoice serializer.
    """
    customer_name = serializers.SerializerMethodField()
    job_order_number = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['invoice_number', 'invoice_date', 'updated_at', 'balance_due']
    
    def get_customer_name(self, obj):
        return obj.customer.full_name
    
    def get_job_order_number(self, obj):
        if obj.job_order:
            return obj.job_order.job_number
        return None
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class InvoiceDetailSerializer(InvoiceSerializer):
    """
    Detailed Invoice serializer with related data.
    """
    customer = CustomerSerializer(read_only=True)
    job_order = JobOrderSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)
    
    class Meta(InvoiceSerializer.Meta):
        fields = InvoiceSerializer.Meta.fields + ['customer', 'job_order', 'created_by', 'items']


class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment serializer.
    """
    customer_name = serializers.SerializerMethodField()
    invoice_number = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    processed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['payment_number', 'payment_date']
    
    def get_customer_name(self, obj):
        return obj.customer.full_name
    
    def get_invoice_number(self, obj):
        return obj.invoice.invoice_number
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None
    
    def get_processed_by_name(self, obj):
        if obj.processed_by:
            return obj.processed_by.get_full_name()
        return None


class PaymentDetailSerializer(PaymentSerializer):
    """
    Detailed Payment serializer with related data.
    """
    customer = CustomerSerializer(read_only=True)
    invoice = InvoiceSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    processed_by = UserSerializer(read_only=True)
    
    class Meta(PaymentSerializer.Meta):
        fields = PaymentSerializer.Meta.fields + ['customer', 'invoice', 'created_by', 'processed_by']


class SupplierPaymentSerializer(serializers.ModelSerializer):
    """
    Supplier Payment serializer.
    """
    supplier_name = serializers.SerializerMethodField()
    purchase_order_number = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    processed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SupplierPayment
        fields = '__all__'
        read_only_fields = ['payment_number', 'payment_date']
    
    def get_supplier_name(self, obj):
        return obj.supplier.name
    
    def get_purchase_order_number(self, obj):
        if obj.purchase_order:
            return obj.purchase_order.po_number
        return None
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None
    
    def get_processed_by_name(self, obj):
        if obj.processed_by:
            return obj.processed_by.get_full_name()
        return None


class SupplierPaymentDetailSerializer(SupplierPaymentSerializer):
    """
    Detailed Supplier Payment serializer with related data.
    """
    supplier = SupplierSerializer(read_only=True)
    purchase_order = PurchaseOrderSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    processed_by = UserSerializer(read_only=True)
    
    class Meta(SupplierPaymentSerializer.Meta):
        fields = SupplierPaymentSerializer.Meta.fields + ['supplier', 'purchase_order', 'created_by', 'processed_by']


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Expense serializer.
    """
    created_by_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['expense_number', 'expense_date']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None
    
    def get_approved_by_name(self, obj):
        if obj.approved_by:
            return obj.approved_by.get_full_name()
        return None


class ExpenseDetailSerializer(ExpenseSerializer):
    """
    Detailed Expense serializer with related data.
    """
    created_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    
    class Meta(ExpenseSerializer.Meta):
        fields = ExpenseSerializer.Meta.fields + ['created_by', 'approved_by']


class AccountReceivableSerializer(serializers.ModelSerializer):
    """
    Account Receivable serializer.
    """
    customer_name = serializers.SerializerMethodField()
    invoice_number = serializers.SerializerMethodField()
    
    class Meta:
        model = AccountReceivable
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_customer_name(self, obj):
        return obj.customer.full_name
    
    def get_invoice_number(self, obj):
        return obj.invoice.invoice_number


class AccountPayableSerializer(serializers.ModelSerializer):
    """
    Account Payable serializer.
    """
    supplier_name = serializers.SerializerMethodField()
    purchase_order_number = serializers.SerializerMethodField()
    
    class Meta:
        model = AccountPayable
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_supplier_name(self, obj):
        return obj.supplier.name
    
    def get_purchase_order_number(self, obj):
        return obj.purchase_order.po_number

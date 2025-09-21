"""
Accounting models for Car ERP System.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from customers.models import Customer
from job_orders.models import JobOrder
from inventory.models import PurchaseOrder, Supplier

User = get_user_model()


class Invoice(models.Model):
    """
    Invoice model.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_TERMS_CHOICES = [
        ('due_on_receipt', 'Due on Receipt'),
        ('net_15', 'Net 15'),
        ('net_30', 'Net 30'),
        ('net_45', 'Net 45'),
        ('net_60', 'Net 60'),
    ]
    
    # Invoice Information
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    job_order = models.ForeignKey(JobOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    
    # Invoice Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    payment_terms = models.CharField(max_length=20, choices=PAYMENT_TERMS_CHOICES, default='due_on_receipt')
    
    # Dates
    invoice_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    paid_date = models.DateTimeField(blank=True, null=True)
    
    # Financial Information
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Tax rate percentage
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_invoices')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-invoice_date']
    
    def __str__(self):
        return f"INV-{self.invoice_number} - {self.customer.full_name}"
    
    def save(self, *args, **kwargs):
        """Generate invoice number if not provided."""
        if not self.invoice_number:
            from datetime import datetime
            now = datetime.now()
            prefix = f"INV{now.year}{now.month:02d}"
            last_invoice = Invoice.objects.filter(invoice_number__startswith=prefix).order_by('-invoice_number').first()
            if last_invoice:
                last_number = int(last_invoice.invoice_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.invoice_number = f"{prefix}{new_number:04d}"
        
        # Calculate due date based on payment terms
        if not self.due_date and self.payment_terms:
            from datetime import timedelta
            days = {
                'due_on_receipt': 0,
                'net_15': 15,
                'net_30': 30,
                'net_45': 45,
                'net_60': 60,
            }
            self.due_date = self.invoice_date + timedelta(days=days.get(self.payment_terms, 0))
        
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    """
    Items in an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    
    # Item Details
    description = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'invoice_items'
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description}"
    
    def save(self, *args, **kwargs):
        """Calculate total price."""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Payment(models.Model):
    """
    Payment model.
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Payment Information
    payment_number = models.CharField(max_length=50, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    
    # Payment Details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Transaction Details
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Dates
    payment_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_payments')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payments')
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"PAY-{self.payment_number} - {self.customer.full_name} ({self.amount})"
    
    def save(self, *args, **kwargs):
        """Generate payment number if not provided."""
        if not self.payment_number:
            from datetime import datetime
            now = datetime.now()
            prefix = f"PAY{now.year}{now.month:02d}"
            last_payment = Payment.objects.filter(payment_number__startswith=prefix).order_by('-payment_number').first()
            if last_payment:
                last_number = int(last_payment.payment_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.payment_number = f"{prefix}{new_number:04d}"
        super().save(*args, **kwargs)


class SupplierPayment(models.Model):
    """
    Supplier payment model.
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Payment Information
    payment_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='payments')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    
    # Payment Details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Transaction Details
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    check_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Dates
    payment_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    processed_date = models.DateTimeField(blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_supplier_payments')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_supplier_payments')
    
    class Meta:
        db_table = 'supplier_payments'
        verbose_name = 'Supplier Payment'
        verbose_name_plural = 'Supplier Payments'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"SPAY-{self.payment_number} - {self.supplier.name} ({self.amount})"
    
    def save(self, *args, **kwargs):
        """Generate payment number if not provided."""
        if not self.payment_number:
            from datetime import datetime
            now = datetime.now()
            prefix = f"SPAY{now.year}{now.month:02d}"
            last_payment = SupplierPayment.objects.filter(payment_number__startswith=prefix).order_by('-payment_number').first()
            if last_payment:
                last_number = int(last_payment.payment_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.payment_number = f"{prefix}{new_number:04d}"
        super().save(*args, **kwargs)


class Expense(models.Model):
    """
    Expense model for tracking business expenses.
    """
    CATEGORY_CHOICES = [
        ('utilities', 'Utilities'),
        ('rent', 'Rent'),
        ('salaries', 'Salaries'),
        ('equipment', 'Equipment'),
        ('maintenance', 'Maintenance'),
        ('marketing', 'Marketing'),
        ('travel', 'Travel'),
        ('office_supplies', 'Office Supplies'),
        ('insurance', 'Insurance'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]
    
    # Expense Information
    expense_number = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Dates
    expense_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    paid_date = models.DateTimeField(blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    receipt = models.FileField(upload_to='expense_receipts/', blank=True, null=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_expenses')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses')
    
    class Meta:
        db_table = 'expenses'
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-expense_date']
    
    def __str__(self):
        return f"EXP-{self.expense_number} - {self.description} ({self.amount})"
    
    def save(self, *args, **kwargs):
        """Generate expense number if not provided."""
        if not self.expense_number:
            from datetime import datetime
            now = datetime.now()
            prefix = f"EXP{now.year}{now.month:02d}"
            last_expense = Expense.objects.filter(expense_number__startswith=prefix).order_by('-expense_number').first()
            if last_expense:
                last_number = int(last_expense.expense_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.expense_number = f"{prefix}{new_number:04d}"
        super().save(*args, **kwargs)


class AccountReceivable(models.Model):
    """
    Account receivable model for tracking customer debts.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='receivables')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='receivables')
    
    # Financial Information
    original_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Dates
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'accounts_receivable'
        verbose_name = 'Account Receivable'
        verbose_name_plural = 'Accounts Receivable'
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.invoice.invoice_number} ({self.current_amount})"


class AccountPayable(models.Model):
    """
    Account payable model for tracking supplier debts.
    """
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='payables')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='payables')
    
    # Financial Information
    original_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Dates
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'accounts_payable'
        verbose_name = 'Account Payable'
        verbose_name_plural = 'Accounts Payable'
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.purchase_order.po_number} ({self.current_amount})"


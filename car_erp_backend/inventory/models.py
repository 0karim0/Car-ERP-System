"""
Inventory models for Car ERP System.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Category(models.Model):
    """
    Parts category model.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Supplier(models.Model):
    """
    Supplier information model.
    """
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    
    # Address Information
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    
    # Business Information
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_suppliers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'suppliers'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Part(models.Model):
    """
    Parts/Spare parts model.
    """
    UNIT_CHOICES = [
        ('piece', 'Piece'),
        ('kg', 'Kilogram'),
        ('liter', 'Liter'),
        ('meter', 'Meter'),
        ('box', 'Box'),
        ('set', 'Set'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    sku = models.CharField(max_length=100, unique=True, verbose_name='SKU')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    part_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Category and Supplier
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='parts')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='parts')
    
    # Pricing Information
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Inventory Information
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    reorder_point = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    reorder_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1, validators=[MinValueValidator(0.01)])
    
    # Unit Information
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='piece')
    
    # Additional Information
    location = models.CharField(max_length=100, blank=True, null=True, help_text='Warehouse location')
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_parts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'parts'
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.sku} - {self.name}"
    
    @property
    def is_low_stock(self):
        """Check if part is below minimum stock level."""
        return self.current_stock <= self.minimum_stock
    
    @property
    def needs_reorder(self):
        """Check if part needs to be reordered."""
        return self.current_stock <= self.reorder_point
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage."""
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0


class PartPhoto(models.Model):
    """
    Part photos for visual reference.
    """
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='part_photos/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'part_photos'
        verbose_name = 'Part Photo'
        verbose_name_plural = 'Part Photos'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.part.name} - {self.title}"


class PurchaseOrder(models.Model):
    """
    Purchase order model.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('confirmed', 'Confirmed'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Purchase Order Information
    po_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Dates
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery = models.DateTimeField(blank=True, null=True)
    actual_delivery = models.DateTimeField(blank=True, null=True)
    
    # Financial Information
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_purchase_orders')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'purchase_orders'
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-order_date']
    
    def __str__(self):
        return f"PO-{self.po_number} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        """Generate PO number if not provided."""
        if not self.po_number:
            from datetime import datetime
            now = datetime.now()
            prefix = f"PO{now.year}{now.month:02d}"
            last_po = PurchaseOrder.objects.filter(po_number__startswith=prefix).order_by('-po_number').first()
            if last_po:
                last_number = int(last_po.po_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.po_number = f"{prefix}{new_number:04d}"
        super().save(*args, **kwargs)


class PurchaseOrderItem(models.Model):
    """
    Items in a purchase order.
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='purchase_order_items')
    
    # Item Details
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'purchase_order_items'
        verbose_name = 'Purchase Order Item'
        verbose_name_plural = 'Purchase Order Items'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.part.name}"
    
    def save(self, *args, **kwargs):
        """Calculate total cost."""
        self.total_cost = self.quantity_ordered * self.unit_cost
        super().save(*args, **kwargs)


class StockMovement(models.Model):
    """
    Stock movement history.
    """
    MOVEMENT_TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
        ('return', 'Return'),
        ('damage', 'Damage'),
        ('other', 'Other'),
    ]
    
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    
    # Movement Details
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    previous_stock = models.DecimalField(max_digits=10, decimal_places=2)
    new_stock = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Reference Information
    reference_type = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'job_order', 'purchase_order'
    reference_id = models.IntegerField(blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'stock_movements'
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.part.name} - {self.get_movement_type_display()} ({self.quantity})"


"""
Job Order models for Car ERP System.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from customers.models import Customer
from vehicles.models import Vehicle

User = get_user_model()


class JobOrder(models.Model):
    """
    Job Order/Work Order model.
    """
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('inspection', 'Inspection'),
        ('waiting_parts', 'Waiting for Parts'),
        ('in_repair', 'In Repair'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Job Order Information
    job_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='job_orders')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='job_orders')
    
    # Service Information
    service_type = models.CharField(max_length=200)
    description = models.TextField()
    customer_complaint = models.TextField(help_text="Customer's description of the problem")
    
    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Dates and Times
    received_date = models.DateTimeField(auto_now_add=True)
    estimated_completion = models.DateTimeField(blank=True, null=True)
    actual_completion = models.DateTimeField(blank=True, null=True)
    
    # Assignment
    assigned_technician = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_job_orders',
        limit_choices_to={'role': 'technician'}
    )
    
    # Financial Information
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True, help_text="Internal notes (not visible to customer)")
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_job_orders')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'job_orders'
        verbose_name = 'Job Order'
        verbose_name_plural = 'Job Orders'
        ordering = ['-received_date']
    
    def __str__(self):
        return f"{self.job_number} - {self.customer.full_name} ({self.vehicle.license_plate})"
    
    def save(self, *args, **kwargs):
        """Generate job number if not provided."""
        if not self.job_number:
            # Generate job number: JO + year + month + sequential number
            from datetime import datetime
            now = datetime.now()
            prefix = f"JO{now.year}{now.month:02d}"
            last_order = JobOrder.objects.filter(job_number__startswith=prefix).order_by('-job_number').first()
            if last_order:
                last_number = int(last_order.job_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.job_number = f"{prefix}{new_number:04d}"
        super().save(*args, **kwargs)


class JobOrderItem(models.Model):
    """
    Items (parts/services) in a job order.
    """
    ITEM_TYPE_CHOICES = [
        ('part', 'Part'),
        ('labor', 'Labor'),
        ('service', 'Service'),
        ('other', 'Other'),
    ]
    
    job_order = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    
    # Item Details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    
    # Quantities and Pricing
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Labor Specific
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'job_order_items'
        verbose_name = 'Job Order Item'
        verbose_name_plural = 'Job Order Items'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.job_order.job_number} - {self.name}"
    
    def save(self, *args, **kwargs):
        """Calculate total price."""
        if self.item_type == 'labor' and self.hours_worked and self.hourly_rate:
            self.total_price = self.hours_worked * self.hourly_rate
        else:
            self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class TechnicianTime(models.Model):
    """
    Technician time tracking for job orders.
    """
    job_order = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name='technician_times')
    technician = models.ForeignKey(User, on_delete=models.CASCADE, related_name='technician_times')
    
    # Time Tracking
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Work Details
    work_description = models.TextField()
    parts_used = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'technician_times'
        verbose_name = 'Technician Time'
        verbose_name_plural = 'Technician Times'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.technician.get_full_name()} - {self.job_order.job_number}"
    
    def save(self, *args, **kwargs):
        """Calculate hours worked."""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.hours_worked = delta.total_seconds() / 3600  # Convert to hours
        super().save(*args, **kwargs)


class JobOrderPhoto(models.Model):
    """
    Photos related to job orders.
    """
    PHOTO_TYPES = [
        ('before', 'Before Repair'),
        ('during', 'During Repair'),
        ('after', 'After Repair'),
        ('damage', 'Damage Documentation'),
        ('part', 'Part Replacement'),
        ('other', 'Other'),
    ]
    
    job_order = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name='photos')
    photo_type = models.CharField(max_length=20, choices=PHOTO_TYPES)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='job_order_photos/')
    description = models.TextField(blank=True, null=True)
    taken_at = models.DateTimeField(auto_now_add=True)
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'job_order_photos'
        verbose_name = 'Job Order Photo'
        verbose_name_plural = 'Job Order Photos'
        ordering = ['-taken_at']
    
    def __str__(self):
        return f"{self.job_order.job_number} - {self.title}"


class JobOrderStatusHistory(models.Model):
    """
    History of status changes for job orders.
    """
    job_order = models.ForeignKey(JobOrder, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20, choices=JobOrder.STATUS_CHOICES, blank=True, null=True)
    new_status = models.CharField(max_length=20, choices=JobOrder.STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'job_order_status_history'
        verbose_name = 'Job Order Status History'
        verbose_name_plural = 'Job Order Status Histories'
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.job_order.job_number} - {self.old_status} → {self.new_status}"


"""
Vehicle models for Car ERP System.
"""
from django.db import models
from django.contrib.auth import get_user_model
from customers.models import Customer

User = get_user_model()


class Vehicle(models.Model):
    """
    Vehicle information model.
    """
    FUEL_TYPE_CHOICES = [
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
        ('lpg', 'LPG'),
        ('cng', 'CNG'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('cvt', 'CVT'),
        ('semi_automatic', 'Semi-Automatic'),
    ]
    
    # Vehicle Identification
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True, verbose_name='VIN/Chassis Number')
    license_plate = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=50)
    
    # Vehicle Specifications
    engine_size = models.CharField(max_length=50, blank=True, null=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, default='gasoline')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='automatic')
    mileage = models.IntegerField(default=0, help_text='Current mileage in miles/km')
    engine_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Ownership Information
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')
    registration_date = models.DateField(blank=True, null=True)
    insurance_expiry = models.DateField(blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_vehicles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        ordering = ['-created_at']
        unique_together = ['vin', 'license_plate']
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.license_plate}"
    
    @property
    def full_description(self):
        return f"{self.year} {self.make} {self.model} ({self.license_plate})"


class VehicleDocument(models.Model):
    """
    Vehicle documents and files.
    """
    DOCUMENT_TYPES = [
        ('registration', 'Registration Certificate'),
        ('insurance', 'Insurance Certificate'),
        ('inspection', 'Inspection Certificate'),
        ('warranty', 'Warranty Certificate'),
        ('manual', 'Owner Manual'),
        ('other', 'Other'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='vehicle_documents/')
    description = models.TextField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'vehicle_documents'
        verbose_name = 'Vehicle Document'
        verbose_name_plural = 'Vehicle Documents'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.vehicle.full_description} - {self.title}"


class VehiclePhoto(models.Model):
    """
    Vehicle photos for visual reference.
    """
    PHOTO_TYPES = [
        ('exterior_front', 'Exterior Front'),
        ('exterior_rear', 'Exterior Rear'),
        ('exterior_side', 'Exterior Side'),
        ('interior_front', 'Interior Front'),
        ('interior_rear', 'Interior Rear'),
        ('engine', 'Engine'),
        ('damage', 'Damage'),
        ('before_repair', 'Before Repair'),
        ('after_repair', 'After Repair'),
        ('other', 'Other'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='photos')
    photo_type = models.CharField(max_length=20, choices=PHOTO_TYPES)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='vehicle_photos/')
    description = models.TextField(blank=True, null=True)
    taken_at = models.DateTimeField(auto_now_add=True)
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'vehicle_photos'
        verbose_name = 'Vehicle Photo'
        verbose_name_plural = 'Vehicle Photos'
        ordering = ['-taken_at']
    
    def __str__(self):
        return f"{self.vehicle.full_description} - {self.title}"


class VehicleHistory(models.Model):
    """
    Vehicle service and maintenance history.
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='history')
    service_date = models.DateTimeField()
    service_type = models.CharField(max_length=200)
    description = models.TextField()
    mileage_at_service = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    service_provider = models.CharField(max_length=200, blank=True, null=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vehicle_history'
        verbose_name = 'Vehicle History'
        verbose_name_plural = 'Vehicle History'
        ordering = ['-service_date']
    
    def __str__(self):
        return f"{self.vehicle.full_description} - {self.service_type} ({self.service_date.strftime('%Y-%m-%d')})"


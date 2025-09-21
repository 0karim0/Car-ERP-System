"""
Customer models for Car ERP System.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Customer(models.Model):
    """
    Customer information model.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Personal Information
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Address Information
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    
    # Business Information
    company_name = models.CharField(max_length=200, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    preferred_contact_method = models.CharField(
        max_length=10, 
        choices=[('phone', 'Phone'), ('email', 'Email'), ('sms', 'SMS')],
        default='phone'
    )
    is_active = models.BooleanField(default=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_address(self):
        address_parts = [self.address_line1]
        if self.address_line2:
            address_parts.append(self.address_line2)
        address_parts.extend([self.city, self.state, self.postal_code])
        return ', '.join(address_parts)


class CustomerDocument(models.Model):
    """
    Customer documents and files.
    """
    DOCUMENT_TYPES = [
        ('license', 'Driver License'),
        ('insurance', 'Insurance Card'),
        ('registration', 'Vehicle Registration'),
        ('other', 'Other'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='customer_documents/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'customer_documents'
        verbose_name = 'Customer Document'
        verbose_name_plural = 'Customer Documents'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.title}"


class CustomerCommunication(models.Model):
    """
    Customer communication history.
    """
    COMMUNICATION_TYPES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('visit', 'In-Person Visit'),
        ('other', 'Other'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='communications')
    communication_type = models.CharField(max_length=10, choices=COMMUNICATION_TYPES)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    direction = models.CharField(
        max_length=10, 
        choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')],
        default='outbound'
    )
    communication_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'customer_communications'
        verbose_name = 'Customer Communication'
        verbose_name_plural = 'Customer Communications'
        ordering = ['-communication_date']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.get_communication_type_display()}"


class Appointment(models.Model):
    """
    Customer appointments.
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    service_type = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_appointments')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'appointments'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['appointment_date']
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"


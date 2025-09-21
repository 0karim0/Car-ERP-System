"""
Authentication models for Car ERP System.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based permissions.
    """
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('receptionist', 'Receptionist'),
        ('technician', 'Technician'),
        ('inventory_manager', 'Inventory Manager'),
        ('accountant', 'Accountant'),
    ]
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_super_admin(self):
        return self.role == 'super_admin'
    
    def is_receptionist(self):
        return self.role == 'receptionist'
    
    def is_technician(self):
        return self.role == 'technician'
    
    def is_inventory_manager(self):
        return self.role == 'inventory_manager'
    
    def is_accountant(self):
        return self.role == 'accountant'
    
    def can_access_crm(self):
        """Check if user can access CRM module."""
        return self.role in ['super_admin', 'receptionist']
    
    def can_access_workshop(self):
        """Check if user can access workshop module."""
        return self.role in ['super_admin', 'technician', 'receptionist']
    
    def can_access_inventory(self):
        """Check if user can access inventory module."""
        return self.role in ['super_admin', 'inventory_manager', 'technician']
    
    def can_access_accounting(self):
        """Check if user can access accounting module."""
        return self.role in ['super_admin', 'accountant']
    
    def can_access_reports(self):
        """Check if user can access reports module."""
        return self.role in ['super_admin', 'accountant']


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} Profile"


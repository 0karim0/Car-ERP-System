"""
Reports models for Car ERP System.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Report(models.Model):
    """
    Report model for storing generated reports.
    """
    REPORT_TYPES = [
        ('sales', 'Sales Report'),
        ('inventory', 'Inventory Report'),
        ('customer', 'Customer Report'),
        ('technician', 'Technician Productivity Report'),
        ('financial', 'Financial Report'),
        ('custom', 'Custom Report'),
    ]
    
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]
    
    # Report Information
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    
    # Report Content
    description = models.TextField(blank=True, null=True)
    parameters = models.JSONField(default=dict, blank=True)  # Store report parameters
    file_path = models.CharField(max_length=500, blank=True, null=True)
    
    # Status
    is_generated = models.BooleanField(default=False)
    generation_status = models.CharField(max_length=20, default='pending')
    
    # System Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    generated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'reports'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"


"""
URL configuration for reports app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Report endpoints
    path('', views.ReportListView.as_view(), name='report_list'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    
    # Report generation endpoints
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('sales-report/', views.sales_report, name='sales_report'),
    path('inventory-report/', views.inventory_report, name='inventory_report'),
    path('technician-performance/', views.technician_performance, name='technician_performance'),
    path('generate/', views.generate_report, name='generate_report'),
]

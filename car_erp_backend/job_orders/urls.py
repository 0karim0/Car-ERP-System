"""
URL configuration for job_orders app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Job Order endpoints
    path('', views.JobOrderListView.as_view(), name='job_order_list'),
    path('<int:pk>/', views.JobOrderDetailView.as_view(), name='job_order_detail'),
    path('<int:pk>/update-status/', views.update_job_order_status, name='update_job_order_status'),
    path('stats/', views.job_order_stats, name='job_order_stats'),
    
    # Job Order Item endpoints
    path('items/', views.JobOrderItemListView.as_view(), name='job_order_item_list'),
    path('items/<int:pk>/', views.JobOrderItemDetailView.as_view(), name='job_order_item_detail'),
    
    # Technician Time endpoints
    path('technician-times/', views.TechnicianTimeListView.as_view(), name='technician_time_list'),
    path('technician-times/<int:pk>/', views.TechnicianTimeDetailView.as_view(), name='technician_time_detail'),
    
    # Job Order Photo endpoints
    path('photos/', views.JobOrderPhotoListView.as_view(), name='job_order_photo_list'),
    path('photos/<int:pk>/', views.JobOrderPhotoDetailView.as_view(), name='job_order_photo_detail'),
]

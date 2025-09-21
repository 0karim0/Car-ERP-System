"""
URL configuration for customers app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Customer endpoints
    path('', views.CustomerListView.as_view(), name='customer_list'),
    path('<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('stats/', views.customer_stats, name='customer_stats'),
    
    # Customer document endpoints
    path('documents/', views.CustomerDocumentListView.as_view(), name='customer_document_list'),
    path('documents/<int:pk>/', views.CustomerDocumentDetailView.as_view(), name='customer_document_detail'),
    
    # Customer communication endpoints
    path('communications/', views.CustomerCommunicationListView.as_view(), name='customer_communication_list'),
    path('communications/<int:pk>/', views.CustomerCommunicationDetailView.as_view(), name='customer_communication_detail'),
    
    # Appointment endpoints
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
]


"""
URL configuration for vehicles app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Vehicle endpoints
    path('', views.VehicleListView.as_view(), name='vehicle_list'),
    path('<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('stats/', views.vehicle_stats, name='vehicle_stats'),
    
    # Vehicle document endpoints
    path('documents/', views.VehicleDocumentListView.as_view(), name='vehicle_document_list'),
    path('documents/<int:pk>/', views.VehicleDocumentDetailView.as_view(), name='vehicle_document_detail'),
    
    # Vehicle photo endpoints
    path('photos/', views.VehiclePhotoListView.as_view(), name='vehicle_photo_list'),
    path('photos/<int:pk>/', views.VehiclePhotoDetailView.as_view(), name='vehicle_photo_detail'),
    
    # Vehicle history endpoints
    path('history/', views.VehicleHistoryListView.as_view(), name='vehicle_history_list'),
    path('history/<int:pk>/', views.VehicleHistoryDetailView.as_view(), name='vehicle_history_detail'),
]

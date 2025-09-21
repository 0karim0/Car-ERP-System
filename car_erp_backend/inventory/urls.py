"""
URL configuration for inventory app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Category endpoints
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Supplier endpoints
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    
    # Part endpoints
    path('parts/', views.PartListView.as_view(), name='part_list'),
    path('parts/<int:pk>/', views.PartDetailView.as_view(), name='part_detail'),
    
    # Part photo endpoints
    path('parts/photos/', views.PartPhotoListView.as_view(), name='part_photo_list'),
    path('parts/photos/<int:pk>/', views.PartPhotoDetailView.as_view(), name='part_photo_detail'),
    
    # Purchase Order endpoints
    path('purchase-orders/', views.PurchaseOrderListView.as_view(), name='purchase_order_list'),
    path('purchase-orders/<int:pk>/', views.PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),
    
    # Purchase Order Item endpoints
    path('purchase-order-items/', views.PurchaseOrderItemListView.as_view(), name='purchase_order_item_list'),
    path('purchase-order-items/<int:pk>/', views.PurchaseOrderItemDetailView.as_view(), name='purchase_order_item_detail'),
    
    # Stock Movement endpoints
    path('stock-movements/', views.StockMovementListView.as_view(), name='stock_movement_list'),
    path('stock-movements/<int:pk>/', views.StockMovementDetailView.as_view(), name='stock_movement_detail'),
    
    # Statistics endpoints
    path('stats/', views.inventory_stats, name='inventory_stats'),
    path('low-stock-alerts/', views.low_stock_alerts, name='low_stock_alerts'),
]

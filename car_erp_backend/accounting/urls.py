"""
URL configuration for accounting app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Invoice endpoints
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<int:invoice_id>/process-payment/', views.process_payment, name='process_payment'),
    
    # Invoice Item endpoints
    path('invoice-items/', views.InvoiceItemListView.as_view(), name='invoice_item_list'),
    path('invoice-items/<int:pk>/', views.InvoiceItemDetailView.as_view(), name='invoice_item_detail'),
    
    # Payment endpoints
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    
    # Supplier Payment endpoints
    path('supplier-payments/', views.SupplierPaymentListView.as_view(), name='supplier_payment_list'),
    path('supplier-payments/<int:pk>/', views.SupplierPaymentDetailView.as_view(), name='supplier_payment_detail'),
    
    # Expense endpoints
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    
    # Account Receivable endpoints
    path('receivables/', views.AccountReceivableListView.as_view(), name='account_receivable_list'),
    
    # Account Payable endpoints
    path('payables/', views.AccountPayableListView.as_view(), name='account_payable_list'),
    
    # Statistics endpoints
    path('stats/', views.accounting_stats, name='accounting_stats'),
]

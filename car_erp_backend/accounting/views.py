"""
Accounting views for Car ERP System.
"""
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count
from .models import (
    Invoice, InvoiceItem, Payment, SupplierPayment, Expense,
    AccountReceivable, AccountPayable
)
from .serializers import (
    InvoiceSerializer, InvoiceDetailSerializer, InvoiceItemSerializer,
    PaymentSerializer, PaymentDetailSerializer, SupplierPaymentSerializer,
    SupplierPaymentDetailSerializer, ExpenseSerializer, ExpenseDetailSerializer,
    AccountReceivableSerializer, AccountPayableSerializer
)
from authentication.models import User


class InvoiceListView(generics.ListCreateAPIView):
    """
    List all invoices or create a new invoice.
    """
    queryset = Invoice.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer', 'payment_terms']
    search_fields = ['invoice_number', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['invoice_date', 'due_date', 'total_amount']
    ordering = ['-invoice_date']
    
    def get_queryset(self):
        """Filter invoices based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return Invoice.objects.all()
        return Invoice.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InvoiceDetailSerializer
        return InvoiceSerializer
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an invoice.
    """
    queryset = Invoice.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InvoiceDetailSerializer
        return InvoiceSerializer
    
    def get_queryset(self):
        """Filter invoices based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return Invoice.objects.all()
        return Invoice.objects.none()


class InvoiceItemListView(generics.ListCreateAPIView):
    """
    List all invoice items or create a new item.
    """
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['invoice']
    
    def get_queryset(self):
        """Filter items based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return InvoiceItem.objects.all()
        return InvoiceItem.objects.none()


class InvoiceItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an invoice item.
    """
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter items based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return InvoiceItem.objects.all()
        return InvoiceItem.objects.none()


class PaymentListView(generics.ListCreateAPIView):
    """
    List all payments or create a new payment.
    """
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'customer']
    search_fields = ['payment_number', 'customer__first_name', 'customer__last_name', 'invoice__invoice_number']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']
    
    def get_queryset(self):
        """Filter payments based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return Payment.objects.all()
        return Payment.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PaymentDetailSerializer
        return PaymentSerializer
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a payment.
    """
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PaymentDetailSerializer
        return PaymentSerializer
    
    def get_queryset(self):
        """Filter payments based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return Payment.objects.all()
        return Payment.objects.none()


class SupplierPaymentListView(generics.ListCreateAPIView):
    """
    List all supplier payments or create a new payment.
    """
    queryset = SupplierPayment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'supplier']
    search_fields = ['payment_number', 'supplier__name', 'purchase_order__po_number']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']
    
    def get_queryset(self):
        """Filter supplier payments based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return SupplierPayment.objects.all()
        return SupplierPayment.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SupplierPaymentDetailSerializer
        return SupplierPaymentSerializer
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class SupplierPaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a supplier payment.
    """
    queryset = SupplierPayment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SupplierPaymentDetailSerializer
        return SupplierPaymentSerializer
    
    def get_queryset(self):
        """Filter supplier payments based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return SupplierPayment.objects.all()
        return SupplierPayment.objects.none()


class ExpenseListView(generics.ListCreateAPIView):
    """
    List all expenses or create a new expense.
    """
    queryset = Expense.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['expense_number', 'description']
    ordering_fields = ['expense_date', 'amount']
    ordering = ['-expense_date']
    
    def get_queryset(self):
        """Filter expenses based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return Expense.objects.all()
        return Expense.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExpenseDetailSerializer
        return ExpenseSerializer
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an expense.
    """
    queryset = Expense.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExpenseDetailSerializer
        return ExpenseSerializer
    
    def get_queryset(self):
        """Filter expenses based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return Expense.objects.all()
        return Expense.objects.none()


class AccountReceivableListView(generics.ListAPIView):
    """
    List all accounts receivable.
    """
    queryset = AccountReceivable.objects.all()
    serializer_class = AccountReceivableSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['customer']
    ordering_fields = ['due_date', 'current_amount']
    ordering = ['due_date']
    
    def get_queryset(self):
        """Filter accounts receivable based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return AccountReceivable.objects.all()
        return AccountReceivable.objects.none()


class AccountPayableListView(generics.ListAPIView):
    """
    List all accounts payable.
    """
    queryset = AccountPayable.objects.all()
    serializer_class = AccountPayableSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['supplier']
    ordering_fields = ['due_date', 'current_amount']
    ordering = ['due_date']
    
    def get_queryset(self):
        """Filter accounts payable based on user permissions."""
        user = self.request.user
        if user.can_access_accounting():
            return AccountPayable.objects.all()
        return AccountPayable.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def accounting_stats(request):
    """
    Get accounting statistics.
    """
    user = request.user
    if not user.can_access_accounting():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Invoice statistics
    total_invoices = Invoice.objects.count()
    pending_invoices = Invoice.objects.filter(status='sent').count()
    paid_invoices = Invoice.objects.filter(status='paid').count()
    overdue_invoices = Invoice.objects.filter(status='overdue').count()
    
    # Payment statistics
    total_payments = Payment.objects.count()
    total_payment_amount = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    # Receivables and Payables
    total_receivables = AccountReceivable.objects.aggregate(total=Sum('current_amount'))['total'] or 0
    total_payables = AccountPayable.objects.aggregate(total=Sum('current_amount'))['total'] or 0
    
    # Expense statistics
    total_expenses = Expense.objects.count()
    pending_expenses = Expense.objects.filter(status='pending').count()
    approved_expenses = Expense.objects.filter(status='approved').count()
    
    return Response({
        'invoices': {
            'total': total_invoices,
            'pending': pending_invoices,
            'paid': paid_invoices,
            'overdue': overdue_invoices,
        },
        'payments': {
            'total_count': total_payments,
            'total_amount': total_payment_amount,
        },
        'receivables': total_receivables,
        'payables': total_payables,
        'expenses': {
            'total': total_expenses,
            'pending': pending_expenses,
            'approved': approved_expenses,
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def process_payment(request, invoice_id):
    """
    Process a payment for an invoice.
    """
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if not user.can_access_accounting():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    amount = request.data.get('amount')
    payment_method = request.data.get('payment_method')
    transaction_id = request.data.get('transaction_id', '')
    
    if not amount or not payment_method:
        return Response({'error': 'Amount and payment method are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create payment
    payment = Payment.objects.create(
        invoice=invoice,
        customer=invoice.customer,
        amount=amount,
        payment_method=payment_method,
        transaction_id=transaction_id,
        status='completed',
        created_by=user,
        processed_by=user
    )
    
    # Update invoice
    invoice.paid_amount += amount
    invoice.balance_due = invoice.total_amount - invoice.paid_amount
    
    if invoice.balance_due <= 0:
        invoice.status = 'paid'
        invoice.paid_date = payment.payment_date
    
    invoice.save()
    
    return Response({
        'message': 'Payment processed successfully',
        'payment': PaymentSerializer(payment).data,
        'invoice': InvoiceSerializer(invoice).data
    })

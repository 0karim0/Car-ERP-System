"""
Customer views for Car ERP System.
"""
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Customer, CustomerDocument, CustomerCommunication, Appointment
from .serializers import (
    CustomerSerializer, CustomerDetailSerializer, CustomerDocumentSerializer,
    CustomerCommunicationSerializer, AppointmentSerializer
)
from authentication.models import User


class CustomerListView(generics.ListCreateAPIView):
    """
    List all customers or create a new customer.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'city', 'state']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'company_name']
    ordering_fields = ['created_at', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter customers based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return Customer.objects.all()
        return Customer.objects.none()
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a customer.
    """
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerDetailSerializer
        return CustomerSerializer
    
    def get_queryset(self):
        """Filter customers based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return Customer.objects.all()
        return Customer.objects.none()


class CustomerDocumentListView(generics.ListCreateAPIView):
    """
    List all customer documents or create a new document.
    """
    queryset = CustomerDocument.objects.all()
    serializer_class = CustomerDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'document_type']
    
    def get_queryset(self):
        """Filter documents based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return CustomerDocument.objects.all()
        return CustomerDocument.objects.none()
    
    def perform_create(self, serializer):
        """Set the uploaded_by field."""
        serializer.save(uploaded_by=self.request.user)


class CustomerDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a customer document.
    """
    queryset = CustomerDocument.objects.all()
    serializer_class = CustomerDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter documents based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return CustomerDocument.objects.all()
        return CustomerDocument.objects.none()


class CustomerCommunicationListView(generics.ListCreateAPIView):
    """
    List all customer communications or create a new communication.
    """
    queryset = CustomerCommunication.objects.all()
    serializer_class = CustomerCommunicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['customer', 'communication_type', 'direction']
    ordering_fields = ['communication_date']
    ordering = ['-communication_date']
    
    def get_queryset(self):
        """Filter communications based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return CustomerCommunication.objects.all()
        return CustomerCommunication.objects.none()
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class CustomerCommunicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a customer communication.
    """
    queryset = CustomerCommunication.objects.all()
    serializer_class = CustomerCommunicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter communications based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return CustomerCommunication.objects.all()
        return CustomerCommunication.objects.none()


class AppointmentListView(generics.ListCreateAPIView):
    """
    List all appointments or create a new appointment.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['customer', 'status', 'assigned_to']
    ordering_fields = ['appointment_date']
    ordering = ['appointment_date']
    
    def get_queryset(self):
        """Filter appointments based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return Appointment.objects.all()
        return Appointment.objects.none()
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an appointment.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter appointments based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return Appointment.objects.all()
        return Appointment.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def customer_stats(request):
    """
    Get customer statistics.
    """
    user = request.user
    if not user.can_access_crm():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='scheduled').count()
    
    return Response({
        'total_customers': total_customers,
        'active_customers': active_customers,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
    })


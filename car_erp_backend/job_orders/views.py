"""
Job Order views for Car ERP System.
"""
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import JobOrder, JobOrderItem, TechnicianTime, JobOrderPhoto, JobOrderStatusHistory
from .serializers import (
    JobOrderSerializer, JobOrderDetailSerializer, JobOrderCreateSerializer,
    JobOrderItemSerializer, TechnicianTimeSerializer, JobOrderPhotoSerializer,
    JobOrderStatusHistorySerializer
)
from authentication.models import User


class JobOrderListView(generics.ListCreateAPIView):
    """
    List all job orders or create a new job order.
    """
    queryset = JobOrder.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'assigned_technician', 'customer']
    search_fields = ['job_number', 'service_type', 'customer__first_name', 'customer__last_name', 'vehicle__license_plate']
    ordering_fields = ['received_date', 'estimated_completion', 'priority']
    ordering = ['-received_date']
    
    def get_queryset(self):
        """Filter job orders based on user permissions."""
        user = self.request.user
        if user.can_access_workshop():
            return JobOrder.objects.all()
        return JobOrder.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobOrderCreateSerializer
        return JobOrderSerializer
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class JobOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a job order.
    """
    queryset = JobOrder.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return JobOrderDetailSerializer
        return JobOrderSerializer
    
    def get_queryset(self):
        """Filter job orders based on user permissions."""
        user = self.request.user
        if user.can_access_workshop():
            return JobOrder.objects.all()
        return JobOrder.objects.none()
    
    def perform_update(self, serializer):
        """Track status changes."""
        instance = self.get_object()
        old_status = instance.status
        new_status = serializer.validated_data.get('status', old_status)
        
        # Save the updated instance
        updated_instance = serializer.save()
        
        # Create status history entry if status changed
        if old_status != new_status:
            JobOrderStatusHistory.objects.create(
                job_order=updated_instance,
                old_status=old_status,
                new_status=new_status,
                changed_by=self.request.user
            )


class JobOrderItemListView(generics.ListCreateAPIView):
    """
    List all job order items or create a new item.
    """
    queryset = JobOrderItem.objects.all()
    serializer_class = JobOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job_order', 'item_type']
    
    def get_queryset(self):
        """Filter items based on user permissions."""
        user = self.request.user
        if user.can_access_workshop():
            return JobOrderItem.objects.all()
        return JobOrderItem.objects.none()


class JobOrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a job order item.
    """
    queryset = JobOrderItem.objects.all()
    serializer_class = JobOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter items based on user permissions."""
        user = self.request.user
        if user.can_access_workshop():
            return JobOrderItem.objects.all()
        return JobOrderItem.objects.none()


class TechnicianTimeListView(generics.ListCreateAPIView):
    """
    List all technician times or create a new time entry.
    """
    queryset = TechnicianTime.objects.all()
    serializer_class = TechnicianTimeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['job_order', 'technician']
    ordering_fields = ['start_time']
    ordering = ['-start_time']
    
    def get_queryset(self):
        """Filter technician times based on user permissions."""
        user = self.request.user
        if user.can_access_workshop():
            return TechnicianTime.objects.all()
        return TechnicianTime.objects.none()


class TechnicianTimeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a technician time entry.
    """
    queryset = TechnicianTime.objects.all()
    serializer_class = TechnicianTimeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter technician times based on user permissions."""
        user = self.request.user
        if user.can_access_workshop():
            return TechnicianTime.objects.all()
        return TechnicianTime.objects.none()


class JobOrderPhotoListView(generics.ListCreateAPIView):
    """
    List all job order photos or create a new photo.
    """
    queryset = JobOrderPhoto.objects.all()
    serializer_class = JobOrderPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job_order', 'photo_type']
    
    def get_queryset(self):
        """Filter photos based on user permissions."""
        user = self.request.user
        if user.can_access_workshop():
            return JobOrderPhoto.objects.all()
        return JobOrderPhoto.objects.none()
    
    def perform_create(self, serializer):
        """Set the taken_by field."""
        serializer.save(taken_by=self.request.user)


class JobOrderPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a job order photo.
    """
    queryset = JobOrderPhoto.objects.all()
    serializer_class = JobOrderPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter photos based on user permissions."""
        user = self.request.user
        if user.can_access_workshop():
            return JobOrderPhoto.objects.all()
        return JobOrderPhoto.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def job_order_stats(request):
    """
    Get job order statistics.
    """
    user = request.user
    if not user.can_access_workshop():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    total_job_orders = JobOrder.objects.count()
    pending_job_orders = JobOrder.objects.filter(status__in=['received', 'inspection']).count()
    in_repair_job_orders = JobOrder.objects.filter(status='in_repair').count()
    ready_job_orders = JobOrder.objects.filter(status='ready').count()
    
    # Get job orders by status
    job_orders_by_status = JobOrder.objects.values('status').annotate(count=models.Count('id'))
    
    return Response({
        'total_job_orders': total_job_orders,
        'pending_job_orders': pending_job_orders,
        'in_repair_job_orders': in_repair_job_orders,
        'ready_job_orders': ready_job_orders,
        'job_orders_by_status': list(job_orders_by_status),
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_job_order_status(request, pk):
    """
    Update job order status with history tracking.
    """
    try:
        job_order = JobOrder.objects.get(pk=pk)
    except JobOrder.DoesNotExist:
        return Response({'error': 'Job order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if not user.can_access_workshop():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    new_status = request.data.get('status')
    notes = request.data.get('notes', '')
    
    if not new_status:
        return Response({'error': 'Status is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    old_status = job_order.status
    job_order.status = new_status
    job_order.save()
    
    # Create status history entry
    JobOrderStatusHistory.objects.create(
        job_order=job_order,
        old_status=old_status,
        new_status=new_status,
        notes=notes,
        changed_by=user
    )
    
    return Response({
        'message': 'Status updated successfully',
        'job_order': JobOrderSerializer(job_order).data
    })

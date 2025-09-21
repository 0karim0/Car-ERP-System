"""
Vehicle views for Car ERP System.
"""
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Vehicle, VehicleDocument, VehiclePhoto, VehicleHistory
from .serializers import (
    VehicleSerializer, VehicleDetailSerializer, VehicleDocumentSerializer,
    VehiclePhotoSerializer, VehicleHistorySerializer
)
from authentication.models import User


class VehicleListView(generics.ListCreateAPIView):
    """
    List all vehicles or create a new vehicle.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['make', 'model', 'year', 'fuel_type', 'is_active']
    search_fields = ['make', 'model', 'license_plate', 'vin', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['created_at', 'year', 'make', 'model']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter vehicles based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return Vehicle.objects.all()
        return Vehicle.objects.none()
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a vehicle.
    """
    queryset = Vehicle.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VehicleDetailSerializer
        return VehicleSerializer
    
    def get_queryset(self):
        """Filter vehicles based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return Vehicle.objects.all()
        return Vehicle.objects.none()


class VehicleDocumentListView(generics.ListCreateAPIView):
    """
    List all vehicle documents or create a new document.
    """
    queryset = VehicleDocument.objects.all()
    serializer_class = VehicleDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vehicle', 'document_type']
    
    def get_queryset(self):
        """Filter documents based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return VehicleDocument.objects.all()
        return VehicleDocument.objects.none()
    
    def perform_create(self, serializer):
        """Set the uploaded_by field."""
        serializer.save(uploaded_by=self.request.user)


class VehicleDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a vehicle document.
    """
    queryset = VehicleDocument.objects.all()
    serializer_class = VehicleDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter documents based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return VehicleDocument.objects.all()
        return VehicleDocument.objects.none()


class VehiclePhotoListView(generics.ListCreateAPIView):
    """
    List all vehicle photos or create a new photo.
    """
    queryset = VehiclePhoto.objects.all()
    serializer_class = VehiclePhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vehicle', 'photo_type']
    
    def get_queryset(self):
        """Filter photos based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return VehiclePhoto.objects.all()
        return VehiclePhoto.objects.none()
    
    def perform_create(self, serializer):
        """Set the taken_by field."""
        serializer.save(taken_by=self.request.user)


class VehiclePhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a vehicle photo.
    """
    queryset = VehiclePhoto.objects.all()
    serializer_class = VehiclePhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter photos based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return VehiclePhoto.objects.all()
        return VehiclePhoto.objects.none()


class VehicleHistoryListView(generics.ListCreateAPIView):
    """
    List all vehicle history or create a new history entry.
    """
    queryset = VehicleHistory.objects.all()
    serializer_class = VehicleHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['vehicle', 'service_type']
    ordering_fields = ['service_date']
    ordering = ['-service_date']
    
    def get_queryset(self):
        """Filter history based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return VehicleHistory.objects.all()
        return VehicleHistory.objects.none()
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class VehicleHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a vehicle history entry.
    """
    queryset = VehicleHistory.objects.all()
    serializer_class = VehicleHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter history based on user permissions."""
        user = self.request.user
        if user.can_access_crm():
            return VehicleHistory.objects.all()
        return VehicleHistory.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def vehicle_stats(request):
    """
    Get vehicle statistics.
    """
    user = request.user
    if not user.can_access_crm():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    total_vehicles = Vehicle.objects.count()
    active_vehicles = Vehicle.objects.filter(is_active=True).count()
    
    # Get vehicles by make
    vehicles_by_make = Vehicle.objects.values('make').annotate(count=models.Count('id')).order_by('-count')[:5]
    
    # Get vehicles by year
    vehicles_by_year = Vehicle.objects.values('year').annotate(count=models.Count('id')).order_by('-year')[:5]
    
    return Response({
        'total_vehicles': total_vehicles,
        'active_vehicles': active_vehicles,
        'vehicles_by_make': list(vehicles_by_make),
        'vehicles_by_year': list(vehicles_by_year),
    })

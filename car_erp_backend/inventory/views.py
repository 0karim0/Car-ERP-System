"""
Inventory views for Car ERP System.
"""
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import (
    Category, Supplier, Part, PartPhoto, PurchaseOrder, 
    PurchaseOrderItem, StockMovement
)
from .serializers import (
    CategorySerializer, SupplierSerializer, PartSerializer, PartDetailSerializer,
    PartPhotoSerializer, PurchaseOrderSerializer, PurchaseOrderDetailSerializer,
    PurchaseOrderItemSerializer, StockMovementSerializer, StockMovementCreateSerializer
)
from authentication.models import User


class CategoryListView(generics.ListCreateAPIView):
    """
    List all categories or create a new category.
    """
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']
    
    def get_queryset(self):
        """Filter categories based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return Category.objects.filter(parent__isnull=True)
        return Category.objects.none()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter categories based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return Category.objects.all()
        return Category.objects.none()


class SupplierListView(generics.ListCreateAPIView):
    """
    List all suppliers or create a new supplier.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'contact_person', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Filter suppliers based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return Supplier.objects.all()
        return Supplier.objects.none()
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a supplier.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter suppliers based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return Supplier.objects.all()
        return Supplier.objects.none()


class PartListView(generics.ListCreateAPIView):
    """
    List all parts or create a new part.
    """
    queryset = Part.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'supplier', 'is_active', 'is_low_stock']
    search_fields = ['sku', 'name', 'brand', 'model', 'part_number']
    ordering_fields = ['name', 'current_stock', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Filter parts based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return Part.objects.all()
        return Part.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PartDetailSerializer
        return PartSerializer
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class PartDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a part.
    """
    queryset = Part.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PartDetailSerializer
        return PartSerializer
    
    def get_queryset(self):
        """Filter parts based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return Part.objects.all()
        return Part.objects.none()


class PartPhotoListView(generics.ListCreateAPIView):
    """
    List all part photos or create a new photo.
    """
    queryset = PartPhoto.objects.all()
    serializer_class = PartPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['part']
    
    def get_queryset(self):
        """Filter photos based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return PartPhoto.objects.all()
        return PartPhoto.objects.none()
    
    def perform_create(self, serializer):
        """Set the uploaded_by field."""
        serializer.save(uploaded_by=self.request.user)


class PartPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a part photo.
    """
    queryset = PartPhoto.objects.all()
    serializer_class = PartPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter photos based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return PartPhoto.objects.all()
        return PartPhoto.objects.none()


class PurchaseOrderListView(generics.ListCreateAPIView):
    """
    List all purchase orders or create a new purchase order.
    """
    queryset = PurchaseOrder.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['supplier', 'status']
    search_fields = ['po_number', 'supplier__name']
    ordering_fields = ['order_date', 'total_amount']
    ordering = ['-order_date']
    
    def get_queryset(self):
        """Filter purchase orders based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return PurchaseOrder.objects.all()
        return PurchaseOrder.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PurchaseOrderDetailSerializer
        return PurchaseOrderSerializer
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a purchase order.
    """
    queryset = PurchaseOrder.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PurchaseOrderDetailSerializer
        return PurchaseOrderSerializer
    
    def get_queryset(self):
        """Filter purchase orders based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return PurchaseOrder.objects.all()
        return PurchaseOrder.objects.none()


class PurchaseOrderItemListView(generics.ListCreateAPIView):
    """
    List all purchase order items or create a new item.
    """
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['purchase_order', 'part']
    
    def get_queryset(self):
        """Filter items based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return PurchaseOrderItem.objects.all()
        return PurchaseOrderItem.objects.none()


class PurchaseOrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a purchase order item.
    """
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter items based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return PurchaseOrderItem.objects.all()
        return PurchaseOrderItem.objects.none()


class StockMovementListView(generics.ListCreateAPIView):
    """
    List all stock movements or create a new movement.
    """
    queryset = StockMovement.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['part', 'movement_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter stock movements based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return StockMovement.objects.all()
        return StockMovement.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StockMovementCreateSerializer
        return StockMovementSerializer
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class StockMovementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a stock movement.
    """
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter stock movements based on user permissions."""
        user = self.request.user
        if user.can_access_inventory():
            return StockMovement.objects.all()
        return StockMovement.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def inventory_stats(request):
    """
    Get inventory statistics.
    """
    user = request.user
    if not user.can_access_inventory():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    total_parts = Part.objects.count()
    low_stock_parts = Part.objects.filter(current_stock__lte=models.F('minimum_stock')).count()
    out_of_stock_parts = Part.objects.filter(current_stock=0).count()
    total_suppliers = Supplier.objects.filter(is_active=True).count()
    
    # Get parts by category
    parts_by_category = Part.objects.values('category__name').annotate(count=Count('id')).order_by('-count')[:5]
    
    # Get low stock parts
    low_stock_items = Part.objects.filter(current_stock__lte=models.F('minimum_stock')).values(
        'name', 'current_stock', 'minimum_stock'
    )[:10]
    
    return Response({
        'total_parts': total_parts,
        'low_stock_parts': low_stock_parts,
        'out_of_stock_parts': out_of_stock_parts,
        'total_suppliers': total_suppliers,
        'parts_by_category': list(parts_by_category),
        'low_stock_items': list(low_stock_items),
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def low_stock_alerts(request):
    """
    Get low stock alerts.
    """
    user = request.user
    if not user.can_access_inventory():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    low_stock_parts = Part.objects.filter(current_stock__lte=models.F('minimum_stock')).select_related('category', 'supplier')
    
    alerts = []
    for part in low_stock_parts:
        alerts.append({
            'part_id': part.id,
            'part_name': part.name,
            'sku': part.sku,
            'current_stock': part.current_stock,
            'minimum_stock': part.minimum_stock,
            'category': part.category.name if part.category else None,
            'supplier': part.supplier.name if part.supplier else None,
            'needs_reorder': part.needs_reorder,
        })
    
    return Response({
        'alerts': alerts,
        'count': len(alerts),
    })

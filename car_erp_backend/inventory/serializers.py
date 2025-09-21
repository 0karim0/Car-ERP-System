"""
Inventory serializers for Car ERP System.
"""
from rest_framework import serializers
from .models import (
    Category, Supplier, Part, PartPhoto, PurchaseOrder, 
    PurchaseOrderItem, StockMovement
)
from authentication.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer.
    """
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []


class SupplierSerializer(serializers.ModelSerializer):
    """
    Supplier serializer.
    """
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class PartPhotoSerializer(serializers.ModelSerializer):
    """
    Part Photo serializer.
    """
    uploaded_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PartPhoto
        fields = '__all__'
        read_only_fields = ['uploaded_at']
    
    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return obj.uploaded_by.get_full_name()
        return None


class PartSerializer(serializers.ModelSerializer):
    """
    Part serializer.
    """
    category_name = serializers.SerializerMethodField()
    supplier_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    is_low_stock = serializers.ReadOnlyField()
    needs_reorder = serializers.ReadOnlyField()
    profit_margin = serializers.ReadOnlyField()
    
    class Meta:
        model = Part
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return None
    
    def get_supplier_name(self, obj):
        if obj.supplier:
            return obj.supplier.name
        return None
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class PartDetailSerializer(PartSerializer):
    """
    Detailed Part serializer with related data.
    """
    category = CategorySerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    photos = PartPhotoSerializer(many=True, read_only=True)
    
    class Meta(PartSerializer.Meta):
        fields = PartSerializer.Meta.fields + ['category', 'supplier', 'created_by', 'photos']


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    """
    Purchase Order Item serializer.
    """
    part_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'total_cost']
    
    def get_part_name(self, obj):
        return obj.part.name


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
    Purchase Order serializer.
    """
    supplier_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ['po_number', 'order_date', 'updated_at']
    
    def get_supplier_name(self, obj):
        return obj.supplier.name
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class PurchaseOrderDetailSerializer(PurchaseOrderSerializer):
    """
    Detailed Purchase Order serializer with related data.
    """
    supplier = SupplierSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    
    class Meta(PurchaseOrderSerializer.Meta):
        fields = PurchaseOrderSerializer.Meta.fields + ['supplier', 'created_by', 'items']


class StockMovementSerializer(serializers.ModelSerializer):
    """
    Stock Movement serializer.
    """
    part_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = StockMovement
        fields = '__all__'
        read_only_fields = ['created_at']
    
    def get_part_name(self, obj):
        return obj.part.name
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class StockMovementCreateSerializer(serializers.ModelSerializer):
    """
    Stock Movement creation serializer.
    """
    class Meta:
        model = StockMovement
        fields = '__all__'
    
    def create(self, validated_data):
        """Create stock movement and update part stock."""
        part = validated_data['part']
        quantity = validated_data['quantity']
        movement_type = validated_data['movement_type']
        
        # Calculate new stock based on movement type
        if movement_type in ['purchase', 'return', 'adjustment']:
            new_stock = part.current_stock + quantity
        elif movement_type in ['sale', 'damage']:
            new_stock = part.current_stock - quantity
        else:
            new_stock = part.current_stock
        
        # Update part stock
        part.current_stock = new_stock
        part.save()
        
        # Create stock movement
        validated_data['previous_stock'] = part.current_stock - quantity if movement_type in ['purchase', 'return', 'adjustment'] else part.current_stock + quantity
        validated_data['new_stock'] = new_stock
        
        return super().create(validated_data)

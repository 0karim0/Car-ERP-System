"""
Job Order serializers for Car ERP System.
"""
from rest_framework import serializers
from .models import JobOrder, JobOrderItem, TechnicianTime, JobOrderPhoto, JobOrderStatusHistory
from customers.serializers import CustomerSerializer
from vehicles.serializers import VehicleSerializer
from authentication.serializers import UserSerializer


class JobOrderItemSerializer(serializers.ModelSerializer):
    """
    Job Order Item serializer.
    """
    class Meta:
        model = JobOrderItem
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'total_price']


class TechnicianTimeSerializer(serializers.ModelSerializer):
    """
    Technician Time serializer.
    """
    technician_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TechnicianTime
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'hours_worked']
    
    def get_technician_name(self, obj):
        return obj.technician.get_full_name()


class JobOrderPhotoSerializer(serializers.ModelSerializer):
    """
    Job Order Photo serializer.
    """
    taken_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = JobOrderPhoto
        fields = '__all__'
        read_only_fields = ['taken_at']
    
    def get_taken_by_name(self, obj):
        if obj.taken_by:
            return obj.taken_by.get_full_name()
        return None


class JobOrderStatusHistorySerializer(serializers.ModelSerializer):
    """
    Job Order Status History serializer.
    """
    changed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = JobOrderStatusHistory
        fields = '__all__'
        read_only_fields = ['changed_at']
    
    def get_changed_by_name(self, obj):
        if obj.changed_by:
            return obj.changed_by.get_full_name()
        return None


class JobOrderSerializer(serializers.ModelSerializer):
    """
    Job Order serializer.
    """
    customer_name = serializers.SerializerMethodField()
    vehicle_description = serializers.SerializerMethodField()
    assigned_technician_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = JobOrder
        fields = '__all__'
        read_only_fields = ['job_number', 'received_date', 'updated_at']
    
    def get_customer_name(self, obj):
        return obj.customer.full_name
    
    def get_vehicle_description(self, obj):
        return obj.vehicle.full_description
    
    def get_assigned_technician_name(self, obj):
        if obj.assigned_technician:
            return obj.assigned_technician.get_full_name()
        return None
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


class JobOrderDetailSerializer(JobOrderSerializer):
    """
    Detailed Job Order serializer with related data.
    """
    customer = CustomerSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    assigned_technician = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    items = JobOrderItemSerializer(many=True, read_only=True)
    technician_times = TechnicianTimeSerializer(many=True, read_only=True)
    photos = JobOrderPhotoSerializer(many=True, read_only=True)
    status_history = JobOrderStatusHistorySerializer(many=True, read_only=True)
    
    class Meta(JobOrderSerializer.Meta):
        fields = JobOrderSerializer.Meta.fields + [
            'customer', 'vehicle', 'assigned_technician', 'created_by',
            'items', 'technician_times', 'photos', 'status_history'
        ]


class JobOrderCreateSerializer(serializers.ModelSerializer):
    """
    Job Order creation serializer.
    """
    class Meta:
        model = JobOrder
        exclude = ['job_number', 'received_date', 'updated_at']
    
    def create(self, validated_data):
        """Create job order with status history."""
        job_order = super().create(validated_data)
        
        # Create initial status history entry
        JobOrderStatusHistory.objects.create(
            job_order=job_order,
            new_status=job_order.status,
            notes='Job order created',
            changed_by=self.context['request'].user
        )
        
        return job_order

"""
Reports views for Car ERP System.
"""
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Report
from .serializers import ReportSerializer
from authentication.models import User
from customers.models import Customer
from vehicles.models import Vehicle
from job_orders.models import JobOrder
from inventory.models import Part
from accounting.models import Invoice, Payment


class ReportListView(generics.ListCreateAPIView):
    """
    List all reports or create a new report.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'format', 'is_generated']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'generated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter reports based on user permissions."""
        user = self.request.user
        if user.can_access_reports():
            return Report.objects.all()
        return Report.objects.none()
    
    def perform_create(self, serializer):
        """Set the created_by field."""
        serializer.save(created_by=self.request.user)


class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a report.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter reports based on user permissions."""
        user = self.request.user
        if user.can_access_reports():
            return Report.objects.all()
        return Report.objects.none()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """
    Get comprehensive dashboard statistics.
    """
    user = request.user
    if not user.can_access_reports():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Date ranges
    today = timezone.now().date()
    this_month = today.replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)
    this_year = today.replace(month=1, day=1)
    
    # Customer statistics
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    new_customers_this_month = Customer.objects.filter(created_at__date__gte=this_month).count()
    
    # Vehicle statistics
    total_vehicles = Vehicle.objects.count()
    active_vehicles = Vehicle.objects.filter(is_active=True).count()
    
    # Job order statistics
    total_job_orders = JobOrder.objects.count()
    pending_job_orders = JobOrder.objects.filter(status__in=['received', 'inspection']).count()
    in_repair_job_orders = JobOrder.objects.filter(status='in_repair').count()
    completed_job_orders = JobOrder.objects.filter(status='delivered').count()
    
    # Financial statistics
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    monthly_revenue = Payment.objects.filter(payment_date__date__gte=this_month).aggregate(total=Sum('amount'))['total'] or 0
    total_invoices = Invoice.objects.count()
    pending_invoices = Invoice.objects.filter(status='sent').count()
    
    # Inventory statistics
    total_parts = Part.objects.count()
    low_stock_parts = Part.objects.filter(current_stock__lte=models.F('minimum_stock')).count()
    out_of_stock_parts = Part.objects.filter(current_stock=0).count()
    
    # Performance metrics
    avg_repair_time = JobOrder.objects.filter(
        actual_completion__isnull=False,
        received_date__isnull=False
    ).aggregate(
        avg_time=Avg(models.F('actual_completion') - models.F('received_date'))
    )['avg_time']
    
    avg_invoice_value = Invoice.objects.aggregate(avg_value=Avg('total_amount'))['avg_value'] or 0
    
    return Response({
        'customers': {
            'total': total_customers,
            'active': active_customers,
            'new_this_month': new_customers_this_month,
        },
        'vehicles': {
            'total': total_vehicles,
            'active': active_vehicles,
        },
        'job_orders': {
            'total': total_job_orders,
            'pending': pending_job_orders,
            'in_repair': in_repair_job_orders,
            'completed': completed_job_orders,
        },
        'financial': {
            'total_revenue': total_revenue,
            'monthly_revenue': monthly_revenue,
            'total_invoices': total_invoices,
            'pending_invoices': pending_invoices,
            'avg_invoice_value': avg_invoice_value,
        },
        'inventory': {
            'total_parts': total_parts,
            'low_stock_parts': low_stock_parts,
            'out_of_stock_parts': out_of_stock_parts,
        },
        'performance': {
            'avg_repair_time_hours': avg_repair_time.total_seconds() / 3600 if avg_repair_time else 0,
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def sales_report(request):
    """
    Generate sales report with date filtering.
    """
    user = request.user
    if not user.can_access_reports():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Date filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = timezone.now().date() - timedelta(days=30)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()
    
    # Sales data
    sales_data = Payment.objects.filter(
        payment_date__date__range=[start_date, end_date],
        status='completed'
    ).values('payment_date__date').annotate(
        total_amount=Sum('amount'),
        payment_count=Count('id')
    ).order_by('payment_date__date')
    
    # Top customers
    top_customers = Payment.objects.filter(
        payment_date__date__range=[start_date, end_date],
        status='completed'
    ).values('customer__first_name', 'customer__last_name').annotate(
        total_spent=Sum('amount'),
        payment_count=Count('id')
    ).order_by('-total_spent')[:10]
    
    # Payment methods breakdown
    payment_methods = Payment.objects.filter(
        payment_date__date__range=[start_date, end_date],
        status='completed'
    ).values('payment_method').annotate(
        total_amount=Sum('amount'),
        count=Count('id')
    )
    
    return Response({
        'period': {
            'start_date': start_date,
            'end_date': end_date,
        },
        'sales_data': list(sales_data),
        'top_customers': list(top_customers),
        'payment_methods': list(payment_methods),
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def inventory_report(request):
    """
    Generate inventory report.
    """
    user = request.user
    if not user.can_access_reports():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Parts by category
    parts_by_category = Part.objects.values('category__name').annotate(
        count=Count('id'),
        total_value=Sum(models.F('current_stock') * models.F('cost_price'))
    ).order_by('-count')
    
    # Low stock items
    low_stock_items = Part.objects.filter(
        current_stock__lte=models.F('minimum_stock')
    ).values('name', 'sku', 'current_stock', 'minimum_stock', 'supplier__name')
    
    # Most used parts (from job orders)
    most_used_parts = JobOrderItem.objects.filter(
        item_type='part'
    ).values('name').annotate(
        total_quantity=Sum('quantity'),
        total_value=Sum('total_price')
    ).order_by('-total_quantity')[:10]
    
    # Supplier performance
    supplier_performance = Part.objects.values('supplier__name').annotate(
        parts_count=Count('id'),
        total_value=Sum(models.F('current_stock') * models.F('cost_price'))
    ).order_by('-parts_count')
    
    return Response({
        'parts_by_category': list(parts_by_category),
        'low_stock_items': list(low_stock_items),
        'most_used_parts': list(most_used_parts),
        'supplier_performance': list(supplier_performance),
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def technician_performance(request):
    """
    Generate technician performance report.
    """
    user = request.user
    if not user.can_access_reports():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Technician statistics
    technician_stats = JobOrder.objects.filter(
        assigned_technician__isnull=False
    ).values('assigned_technician__first_name', 'assigned_technician__last_name').annotate(
        total_jobs=Count('id'),
        completed_jobs=Count('id', filter=Q(status='delivered')),
        avg_completion_time=Avg(models.F('actual_completion') - models.F('received_date'))
    ).order_by('-total_jobs')
    
    # Time tracking data
    time_tracking = TechnicianTime.objects.values('technician__first_name', 'technician__last_name').annotate(
        total_hours=Sum('hours_worked'),
        jobs_count=Count('job_order', distinct=True)
    ).order_by('-total_hours')
    
    return Response({
        'technician_stats': list(technician_stats),
        'time_tracking': list(time_tracking),
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_report(request):
    """
    Generate a custom report.
    """
    user = request.user
    if not user.can_access_reports():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    report_type = request.data.get('report_type')
    format_type = request.data.get('format', 'json')
    parameters = request.data.get('parameters', {})
    
    if not report_type:
        return Response({'error': 'Report type is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create report record
    report = Report.objects.create(
        name=f"{report_type.title()} Report - {timezone.now().strftime('%Y-%m-%d %H:%M')}",
        report_type=report_type,
        format=format_type,
        parameters=parameters,
        created_by=user,
        generation_status='processing'
    )
    
    try:
        # Generate report data based on type
        if report_type == 'sales':
            data = sales_report(request).data
        elif report_type == 'inventory':
            data = inventory_report(request).data
        elif report_type == 'technician':
            data = technician_performance(request).data
        else:
            data = dashboard_stats(request).data
        
        # Update report status
        report.is_generated = True
        report.generation_status = 'completed'
        report.generated_at = timezone.now()
        report.save()
        
        return Response({
            'message': 'Report generated successfully',
            'report': ReportSerializer(report).data,
            'data': data
        })
        
    except Exception as e:
        report.generation_status = 'failed'
        report.save()
        return Response(
            {'error': f'Report generation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

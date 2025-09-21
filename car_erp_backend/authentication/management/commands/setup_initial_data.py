"""
Management command to set up initial data for Car ERP System.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up initial data for Car ERP System'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        with transaction.atomic():
            # Create super admin user
            self.create_super_admin()
            
            # Create demo users for each role
            self.create_demo_users()
            
            # Create demo categories
            self.create_demo_categories()
            
            # Create demo suppliers
            self.create_demo_suppliers()
            
        self.stdout.write(
            self.style.SUCCESS('Successfully set up initial data!')
        )

    def create_super_admin(self):
        """Create super admin user."""
        admin_email = config('ADMIN_EMAIL', default='admin@carerp.com')
        admin_password = config('ADMIN_PASSWORD', default='admin123')
        
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                username='admin',
                email=admin_email,
                password=admin_password,
                first_name='Super',
                last_name='Admin',
                role='super_admin'
            )
            self.stdout.write(f'Created super admin: {admin_email}')
        else:
            self.stdout.write(f'Super admin already exists: {admin_email}')

    def create_demo_users(self):
        """Create demo users for each role."""
        demo_users = [
            {
                'username': 'receptionist1',
                'email': 'receptionist@carerp.com',
                'password': 'demo123',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'role': 'receptionist',
                'phone': '+1-555-0101'
            },
            {
                'username': 'technician1',
                'email': 'technician@carerp.com',
                'password': 'demo123',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'role': 'technician',
                'phone': '+1-555-0102'
            },
            {
                'username': 'inventory1',
                'email': 'inventory@carerp.com',
                'password': 'demo123',
                'first_name': 'Lisa',
                'last_name': 'Brown',
                'role': 'inventory_manager',
                'phone': '+1-555-0103'
            },
            {
                'username': 'accountant1',
                'email': 'accountant@carerp.com',
                'password': 'demo123',
                'first_name': 'David',
                'last_name': 'Davis',
                'role': 'accountant',
                'phone': '+1-555-0104'
            }
        ]
        
        for user_data in demo_users:
            if not User.objects.filter(email=user_data['email']).exists():
                User.objects.create_user(**user_data)
                self.stdout.write(f'Created demo user: {user_data["email"]} ({user_data["role"]})')
            else:
                self.stdout.write(f'Demo user already exists: {user_data["email"]}')

    def create_demo_categories(self):
        """Create demo categories."""
        from inventory.models import Category
        
        categories_data = [
            {'name': 'Engine Parts', 'description': 'Engine components and accessories'},
            {'name': 'Brake System', 'description': 'Brake pads, rotors, and brake system components'},
            {'name': 'Suspension', 'description': 'Shocks, struts, and suspension components'},
            {'name': 'Electrical', 'description': 'Electrical components and wiring'},
            {'name': 'Body Parts', 'description': 'Body panels, bumpers, and exterior parts'},
            {'name': 'Interior', 'description': 'Interior components and accessories'},
            {'name': 'Filters', 'description': 'Air filters, oil filters, and fuel filters'},
            {'name': 'Fluids', 'description': 'Oils, coolants, and other automotive fluids'},
        ]
        
        for category_data in categories_data:
            if not Category.objects.filter(name=category_data['name']).exists():
                Category.objects.create(**category_data)
                self.stdout.write(f'Created category: {category_data["name"]}')
            else:
                self.stdout.write(f'Category already exists: {category_data["name"]}')

    def create_demo_suppliers(self):
        """Create demo suppliers."""
        from inventory.models import Supplier
        
        suppliers_data = [
            {
                'name': 'Auto Parts Direct',
                'contact_person': 'John Smith',
                'email': 'john@autopartsdirect.com',
                'phone': '+1-555-1001',
                'address_line1': '123 Industrial Blvd',
                'city': 'Detroit',
                'state': 'MI',
                'postal_code': '48201',
                'payment_terms': 'Net 30',
                'credit_limit': 50000.00
            },
            {
                'name': 'Premium Auto Supply',
                'contact_person': 'Mary Johnson',
                'email': 'mary@premiumauto.com',
                'phone': '+1-555-1002',
                'address_line1': '456 Commerce St',
                'city': 'Chicago',
                'state': 'IL',
                'postal_code': '60601',
                'payment_terms': 'Net 15',
                'credit_limit': 75000.00
            },
            {
                'name': 'Fast Track Parts',
                'contact_person': 'Robert Davis',
                'email': 'robert@fasttrack.com',
                'phone': '+1-555-1003',
                'address_line1': '789 Speedway Ave',
                'city': 'Los Angeles',
                'state': 'CA',
                'postal_code': '90001',
                'payment_terms': 'Due on Receipt',
                'credit_limit': 30000.00
            }
        ]
        
        for supplier_data in suppliers_data:
            if not Supplier.objects.filter(name=supplier_data['name']).exists():
                Supplier.objects.create(**supplier_data)
                self.stdout.write(f'Created supplier: {supplier_data["name"]}')
            else:
                self.stdout.write(f'Supplier already exists: {supplier_data["name"]}')

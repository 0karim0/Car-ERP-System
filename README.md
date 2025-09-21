# Car ERP System

A comprehensive Enterprise Resource Planning (ERP) system designed specifically for auto service centers. This integrated solution combines all administrative, operational, and financial processes in one place.

## 🚗 Features

### 📞 Customer Reception & CRM
- Complete customer database with contact information and history
- Vehicle database with detailed specifications and service history
- Job order creation and management
- Customer complaint tracking with photo documentation
- Appointment scheduling system
- Automated customer notifications (SMS/Email)

### 🔧 Workshop & Operations
- Real-time vehicle status tracking through workflow stages:
  - Received → Inspection → Waiting for Parts → In Repair → Ready → Delivered
- Technician time tracking and work documentation
- Parts usage recording
- Photo documentation of work progress
- Status change history tracking

### 📦 Inventory & Spare Parts Management
- Comprehensive parts database with SKU management
- Real-time inventory tracking
- Automatic low stock alerts
- Supplier management and purchase order tracking
- Stock movement history
- Automatic reorder point notifications

### 💰 Accounting & Invoicing
- Automated invoice generation from job orders
- Multiple payment methods (Cash, Card, Transfer)
- Customer receivables tracking
- Supplier payables management
- Expense tracking and approval workflow
- Financial reports and analytics

### 📊 Reports & Analytics
- Performance reports for vehicles and parts
- Technician productivity analysis
- Customer loyalty metrics
- Key Performance Indicators (KPIs)
- Export capabilities (CSV/PDF)
- Real-time dashboard with statistics

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **Database**: PostgreSQL
- **API**: Django REST Framework
- **Authentication**: JWT with role-based permissions
- **Background Tasks**: Celery with Redis
- **Documentation**: Swagger/OpenAPI

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **State Management**: React Query
- **Routing**: React Router DOM
- **UI Components**: Lucide React Icons
- **Notifications**: React Hot Toast

### DevOps
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7
- **File Storage**: Local storage with media handling

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd car-erp-system
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit the `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=car_erp
   DB_USER=postgres
   DB_PASSWORD=password
   ADMIN_EMAIL=admin@carerp.com
   ADMIN_PASSWORD=admin123
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Initialize the database**
   ```bash
   # Wait for containers to be ready, then run:
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py setup_initial_data
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/swagger/

### Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@carerp.com | admin123 |
| Receptionist | receptionist@carerp.com | demo123 |
| Technician | technician@carerp.com | demo123 |
| Inventory Manager | inventory@carerp.com | demo123 |
| Accountant | accountant@carerp.com | demo123 |

## 📱 User Roles & Permissions

### Super Admin
- Full system access
- User management
- System configuration
- All module access

### Receptionist
- Customer management
- Vehicle registration
- Job order creation
- Appointment scheduling

### Technician
- Job order updates
- Time tracking
- Work documentation
- Parts usage recording

### Inventory Manager
- Parts management
- Supplier management
- Purchase orders
- Stock movements

### Accountant
- Invoice generation
- Payment processing
- Financial reports
- Expense management

## 🔧 Development Setup

### Backend Development

1. **Set up Python environment**
   ```bash
   cd car_erp_backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up db redis -d
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   
   # Set up initial data
   python manage.py setup_initial_data
   ```

3. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Frontend Development

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

## 📁 Project Structure

```
car-erp-system/
├── car_erp_backend/          # Django backend
│   ├── authentication/       # User management
│   ├── customers/           # Customer CRM
│   ├── vehicles/            # Vehicle management
│   ├── job_orders/          # Work order management
│   ├── inventory/           # Inventory management
│   ├── accounting/          # Financial management
│   ├── reports/             # Reporting system
│   └── car_erp_backend/     # Main settings
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── contexts/       # React contexts
│   │   └── utils/          # Utility functions
│   └── public/             # Static assets
├── docker-compose.yml       # Docker configuration
├── requirements.txt         # Python dependencies
├── package.json            # Node.js dependencies
└── README.md              # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/update/` - Update user profile

### Customers
- `GET /api/customers/` - List customers
- `POST /api/customers/` - Create customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

### Vehicles
- `GET /api/vehicles/` - List vehicles
- `POST /api/vehicles/` - Create vehicle
- `GET /api/vehicles/{id}/` - Get vehicle details

### Job Orders
- `GET /api/job-orders/` - List job orders
- `POST /api/job-orders/` - Create job order
- `GET /api/job-orders/{id}/` - Get job order details
- `POST /api/job-orders/{id}/update-status/` - Update job order status

### Inventory
- `GET /api/inventory/parts/` - List parts
- `POST /api/inventory/parts/` - Create part
- `GET /api/inventory/suppliers/` - List suppliers
- `GET /api/inventory/low-stock-alerts/` - Get low stock alerts

### Accounting
- `GET /api/accounting/invoices/` - List invoices
- `POST /api/accounting/invoices/` - Create invoice
- `GET /api/accounting/payments/` - List payments

## 🗄️ Database Schema

### Core Tables
- `users` - User accounts and roles
- `customers` - Customer information
- `vehicles` - Vehicle details
- `job_orders` - Work orders
- `job_order_items` - Services/parts in work orders
- `technician_times` - Technician time tracking
- `parts` - Spare parts inventory
- `suppliers` - Supplier information
- `purchase_orders` - Purchase orders
- `invoices` - Customer invoices
- `payments` - Payment records

## 📊 Key Features

### Workflow Management
- Visual status tracking for job orders
- Automated notifications at status changes
- Photo documentation throughout the process
- Time tracking for productivity analysis

### Inventory Control
- Real-time stock levels
- Automatic reorder alerts
- Supplier management
- Purchase order automation
- Stock movement tracking

### Financial Management
- Automated invoice generation
- Multiple payment methods
- Receivables and payables tracking
- Expense management
- Financial reporting

### Reporting & Analytics
- Dashboard with key metrics
- Customizable reports
- Export to CSV/PDF
- Performance analytics
- KPI tracking

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- Secure password handling
- CORS protection
- SQL injection prevention
- XSS protection

## 🚀 Deployment

### Production Deployment

1. **Set up production environment variables**
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=your-domain.com
   DB_HOST=your-db-host
   DB_PASSWORD=your-secure-password
   ```

2. **Build and deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

3. **Run migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py collectstatic --noinput
   ```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Email: support@carerp.com
- Documentation: [API Docs](http://localhost:8000/swagger/)
- Issues: [GitHub Issues](https://github.com/your-repo/issues)

## 🎯 Roadmap

- [ ] Mobile app development
- [ ] Advanced reporting features
- [ ] Integration with external systems
- [ ] Multi-location support
- [ ] Advanced analytics and AI insights
- [ ] Barcode scanning integration
- [ ] SMS/Email automation
- [ ] Customer portal

---

**Car ERP System** - Streamlining auto service center operations with modern technology.

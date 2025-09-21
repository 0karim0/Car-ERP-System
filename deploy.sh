#!/bin/bash

# Car ERP System Deployment Script
echo "🚗 Starting Car ERP System deployment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing."
    read -p "Press Enter after editing .env file..."
fi

# Build and start containers
echo "🏗️  Building and starting containers..."
docker-compose up --build -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🗄️  Running database migrations..."
docker-compose exec backend python manage.py migrate

# Set up initial data
echo "📊 Setting up initial data..."
docker-compose exec backend python manage.py setup_initial_data

# Collect static files
echo "📦 Collecting static files..."
docker-compose exec backend python manage.py collectstatic --noinput

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Access your Car ERP System:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/swagger/"
echo ""
echo "👤 Default login credentials:"
echo "   Super Admin: admin@carerp.com / admin123"
echo "   Receptionist: receptionist@carerp.com / demo123"
echo "   Technician: technician@carerp.com / demo123"
echo "   Inventory Manager: inventory@carerp.com / demo123"
echo "   Accountant: accountant@carerp.com / demo123"
echo ""
echo "📋 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop the system:"
echo "   docker-compose down"

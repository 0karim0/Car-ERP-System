@echo off
REM Car ERP System Deployment Script for Windows
echo 🚗 Starting Car ERP System deployment...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose and try again.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.example .env
    echo ⚠️  Please edit .env file with your configuration before continuing.
    pause
)

REM Build and start containers
echo 🏗️  Building and starting containers...
docker-compose up --build -d

REM Wait for database to be ready
echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM Run migrations
echo 🗄️  Running database migrations...
docker-compose exec backend python manage.py migrate

REM Set up initial data
echo 📊 Setting up initial data...
docker-compose exec backend python manage.py setup_initial_data

REM Collect static files
echo 📦 Collecting static files...
docker-compose exec backend python manage.py collectstatic --noinput

echo ✅ Deployment completed successfully!
echo.
echo 🌐 Access your Car ERP System:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/swagger/
echo.
echo 👤 Default login credentials:
echo    Super Admin: admin@carerp.com / admin123
echo    Receptionist: receptionist@carerp.com / demo123
echo    Technician: technician@carerp.com / demo123
echo    Inventory Manager: inventory@carerp.com / demo123
echo    Accountant: accountant@carerp.com / demo123
echo.
echo 📋 To view logs:
echo    docker-compose logs -f
echo.
echo 🛑 To stop the system:
echo    docker-compose down
pause

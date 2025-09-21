@echo off
REM Car ERP System - Production Deployment Script for Windows
echo 🚗 Starting Car ERP System Production Deployment...

REM This script is for Windows Server or Windows 10/11 with WSL2
echo.
echo ⚠️  WARNING: This script is designed for Linux servers.
echo    For Windows deployment, please use WSL2 or a Linux virtual machine.
echo.
echo Recommended approach:
echo 1. Install WSL2 with Ubuntu
echo 2. Run the Linux deployment script (deploy-production.sh)
echo 3. Or use a cloud provider like DigitalOcean, AWS, or Azure
echo.
echo Alternative Windows deployment options:
echo 1. Use Docker Desktop with WSL2 backend
echo 2. Deploy to cloud providers (DigitalOcean, AWS, Azure)
echo 3. Use Windows Subsystem for Linux (WSL2)
echo.

REM Check if WSL is available
wsl --status >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ WSL is available. You can run the Linux deployment script.
    echo.
    echo To deploy using WSL:
    echo 1. Copy your project to WSL: wsl -d Ubuntu
    echo 2. Navigate to project directory
    echo 3. Run: chmod +x deploy-production.sh && ./deploy-production.sh
    echo.
) else (
    echo ❌ WSL is not available.
    echo.
    echo To install WSL2:
    echo 1. Run as Administrator: wsl --install
    echo 2. Restart your computer
    echo 3. Run this script again
    echo.
)

REM Check if Docker Desktop is installed
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker Desktop is installed.
    echo.
    echo You can deploy using Docker Desktop:
    echo 1. Ensure WSL2 integration is enabled in Docker Desktop
    echo 2. Copy project files to WSL
    echo 3. Run deployment script in WSL
    echo.
) else (
    echo ❌ Docker Desktop is not installed.
    echo.
    echo To install Docker Desktop:
    echo 1. Download from: https://www.docker.com/products/docker-desktop/
    echo 2. Install with WSL2 backend enabled
    echo 3. Restart your computer
    echo.
)

echo 🌐 Cloud Deployment Options:
echo.
echo 1. DigitalOcean (Recommended for beginners):
echo    - Create account at https://digitalocean.com
echo    - Create Ubuntu 22.04 droplet
echo    - Upload your project files
echo    - Run deployment script
echo.
echo 2. AWS EC2:
echo    - Create account at https://aws.amazon.com
echo    - Launch Ubuntu 22.04 instance
echo    - Configure security groups
echo    - Run deployment script
echo.
echo 3. Google Cloud Platform:
echo    - Create account at https://cloud.google.com
echo    - Create Ubuntu 22.04 VM instance
echo    - Configure firewall rules
echo    - Run deployment script
echo.
echo 4. Azure:
echo    - Create account at https://azure.microsoft.com
echo    - Create Ubuntu 22.04 VM
echo    - Configure network security groups
echo    - Run deployment script
echo.

echo 📋 Quick Cloud Deployment Steps:
echo.
echo 1. Choose a cloud provider (DigitalOcean recommended)
echo 2. Create Ubuntu 22.04 server
echo 3. Connect via SSH
echo 4. Upload project files
echo 5. Run: chmod +x deploy-production.sh
echo 6. Run: ./deploy-production.sh
echo 7. Follow the prompts
echo.

echo 🔧 Manual Windows Deployment (Advanced):
echo.
echo If you want to deploy on Windows without WSL:
echo 1. Install Node.js and Python
echo 2. Install PostgreSQL and Redis
echo 3. Configure environment variables
echo 4. Run backend: python manage.py runserver
echo 5. Run frontend: npm start
echo 6. Configure IIS or Apache as reverse proxy
echo.
echo ⚠️  Note: This approach is complex and not recommended.
echo    Use cloud deployment or WSL2 for best results.
echo.

echo 📞 Need Help?
echo.
echo - Check the HOSTING_GUIDE.md for detailed instructions
echo - Visit our documentation for step-by-step guides
echo - Contact support for deployment assistance
echo.

pause

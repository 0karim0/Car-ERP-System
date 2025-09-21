#!/bin/bash

# Car ERP System - Production Deployment Script
echo "🚗 Starting Car ERP System Production Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="car-erp-system"
DOMAIN_NAME=""
EMAIL=""
BACKUP_DIR="/opt/backups"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root (use sudo)"
    exit 1
fi

# Get domain name and email
if [ -z "$DOMAIN_NAME" ]; then
    read -p "Enter your domain name (e.g., example.com): " DOMAIN_NAME
fi

if [ -z "$EMAIL" ]; then
    read -p "Enter your email address for SSL certificate: " EMAIL
fi

print_status "Domain: $DOMAIN_NAME"
print_status "Email: $EMAIL"

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install required packages
print_status "Installing required packages..."
apt install -y curl wget git ufw fail2ban htop nginx certbot python3-certbot-nginx

# Install Docker
print_status "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    print_success "Docker installed successfully"
else
    print_success "Docker is already installed"
fi

# Install Docker Compose
print_status "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed successfully"
else
    print_success "Docker Compose is already installed"
fi

# Configure firewall
print_status "Configuring firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
print_success "Firewall configured"

# Configure fail2ban
print_status "Configuring fail2ban..."
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
maxretry = 3
EOF

systemctl enable fail2ban
systemctl restart fail2ban
print_success "Fail2ban configured"

# Create backup directory
print_status "Creating backup directory..."
mkdir -p $BACKUP_DIR
chmod 755 $BACKUP_DIR

# Check if project directory exists
if [ ! -d "/opt/$PROJECT_NAME" ]; then
    print_status "Creating project directory..."
    mkdir -p /opt/$PROJECT_NAME
    cd /opt/$PROJECT_NAME
    
    # Clone repository (replace with your repository URL)
    print_status "Please provide your Git repository URL:"
    read -p "Git repository URL: " GIT_REPO
    
    if [ ! -z "$GIT_REPO" ]; then
        git clone $GIT_REPO .
        print_success "Repository cloned successfully"
    else
        print_warning "No repository URL provided. Please copy your project files to /opt/$PROJECT_NAME"
        print_status "Waiting for project files..."
        read -p "Press Enter when you have copied the project files..."
    fi
else
    cd /opt/$PROJECT_NAME
    print_status "Updating existing project..."
    git pull origin main
fi

# Configure environment variables
print_status "Configuring environment variables..."
if [ ! -f ".env" ]; then
    cp env.example .env
    print_warning "Please edit .env file with your production settings"
    print_status "Opening .env file for editing..."
    nano .env
fi

# Update nginx configuration with domain name
print_status "Updating nginx configuration..."
sed -i "s/your-domain.com/$DOMAIN_NAME/g" nginx/nginx.conf

# Build and start services
print_status "Building and starting services..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 30

# Run database migrations
print_status "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Collect static files
print_status "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

# Set up initial data
print_status "Setting up initial data..."
docker-compose -f docker-compose.prod.yml exec backend python manage.py setup_initial_data

# Get SSL certificate
print_status "Obtaining SSL certificate..."
certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME --email $EMAIL --agree-tos --non-interactive

# Configure automatic SSL renewal
print_status "Configuring automatic SSL renewal..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

# Create backup script
print_status "Creating backup script..."
cat > /opt/backup.sh << EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
cd /opt/$PROJECT_NAME
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U car_erp_user car_erp_production > $BACKUP_DIR/backup_\$DATE.sql
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
EOF

chmod +x /opt/backup.sh

# Add daily backup to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/backup.sh") | crontab -

# Create monitoring script
print_status "Creating monitoring script..."
cat > /opt/monitor.sh << EOF
#!/bin/bash
cd /opt/$PROJECT_NAME
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "Services down, restarting..." | mail -s "Car ERP System Alert" $EMAIL
    docker-compose -f docker-compose.prod.yml up -d
fi
EOF

chmod +x /opt/monitor.sh

# Add monitoring to crontab
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/monitor.sh") | crontab -

# Check service status
print_status "Checking service status..."
docker-compose -f docker-compose.prod.yml ps

# Final status check
print_status "Performing final status check..."
if curl -f https://$DOMAIN_NAME/health > /dev/null 2>&1; then
    print_success "Application is responding correctly"
else
    print_warning "Application health check failed. Please check the logs:"
    docker-compose -f docker-compose.prod.yml logs --tail=50
fi

# Display completion message
echo ""
print_success "🎉 Car ERP System deployed successfully!"
echo ""
echo -e "${BLUE}Access URLs:${NC}"
echo -e "  Frontend: ${GREEN}https://$DOMAIN_NAME${NC}"
echo -e "  Admin Panel: ${GREEN}https://$DOMAIN_NAME/admin/${NC}"
echo -e "  API Documentation: ${GREEN}https://$DOMAIN_NAME/swagger/${NC}"
echo ""
echo -e "${BLUE}Default Login Credentials:${NC}"
echo -e "  Super Admin: ${YELLOW}admin@carerp.com${NC} / ${YELLOW}admin123${NC}"
echo -e "  Receptionist: ${YELLOW}receptionist@carerp.com${NC} / ${YELLOW}demo123${NC}"
echo -e "  Technician: ${YELLOW}technician@carerp.com${NC} / ${YELLOW}demo123${NC}"
echo -e "  Inventory Manager: ${YELLOW}inventory@carerp.com${NC} / ${YELLOW}demo123${NC}"
echo -e "  Accountant: ${YELLOW}accountant@carerp.com${NC} / ${YELLOW}demo123${NC}"
echo ""
echo -e "${BLUE}Management Commands:${NC}"
echo -e "  View logs: ${YELLOW}docker-compose -f docker-compose.prod.yml logs -f${NC}"
echo -e "  Restart services: ${YELLOW}docker-compose -f docker-compose.prod.yml restart${NC}"
echo -e "  Stop services: ${YELLOW}docker-compose -f docker-compose.prod.yml down${NC}"
echo -e "  Update application: ${YELLOW}git pull && docker-compose -f docker-compose.prod.yml up -d --build${NC}"
echo ""
echo -e "${BLUE}Backup:${NC}"
echo -e "  Manual backup: ${YELLOW}/opt/backup.sh${NC}"
echo -e "  Automatic backups: ${YELLOW}Daily at 2 AM${NC}"
echo ""
echo -e "${RED}⚠️  IMPORTANT SECURITY NOTES:${NC}"
echo -e "  1. Change default passwords immediately"
echo -e "  2. Update .env file with secure passwords"
echo -e "  3. Configure email settings for notifications"
echo -e "  4. Regularly update system packages"
echo -e "  5. Monitor application logs"
echo ""
print_success "Deployment completed successfully!"

# Car ERP System - Server Hosting Guide

## 🌐 Hosting Options Overview

### 1. Cloud Providers (Recommended)
- **AWS (Amazon Web Services)**
- **Google Cloud Platform (GCP)**
- **Microsoft Azure**
- **DigitalOcean**
- **Linode**
- **Vultr**

### 2. VPS (Virtual Private Server)
- **DigitalOcean Droplets**
- **Linode Nanodes**
- **Vultr Cloud Compute**
- **AWS EC2**

### 3. Shared Hosting (Limited)
- **Heroku** (with some modifications)
- **Railway**
- **Render**

## 🚀 Recommended Hosting Setup

### Option 1: DigitalOcean Droplet (Recommended for Beginners)

#### Server Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB+ (8GB recommended)
- **Storage**: 50GB+ SSD
- **OS**: Ubuntu 22.04 LTS
- **Cost**: $20-40/month

#### Step-by-Step Deployment

1. **Create DigitalOcean Account**
   ```bash
   # Visit: https://www.digitalocean.com/
   # Create account and add payment method
   ```

2. **Create Droplet**
   - Choose Ubuntu 22.04 LTS
   - Select 4GB RAM plan
   - Add SSH key or password
   - Choose datacenter region

3. **Connect to Server**
   ```bash
   ssh root@your-server-ip
   ```

4. **Update System**
   ```bash
   apt update && apt upgrade -y
   ```

5. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

6. **Install Docker Compose**
   ```bash
   apt install docker-compose -y
   ```

7. **Clone Your Project**
   ```bash
   git clone your-repository-url
   cd car-erp-system
   ```

8. **Configure Environment**
   ```bash
   cp env.example .env
   nano .env
   ```

9. **Deploy Application**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

10. **Configure Firewall**
    ```bash
    ufw allow 22    # SSH
    ufw allow 80    # HTTP
    ufw allow 443   # HTTPS
    ufw enable
    ```

### Option 2: AWS EC2 Deployment

#### Server Requirements
- **Instance Type**: t3.medium or larger
- **Storage**: 30GB+ EBS
- **Security Groups**: HTTP (80), HTTPS (443), SSH (22)
- **Cost**: $30-60/month

#### Deployment Steps

1. **Launch EC2 Instance**
   - Choose Ubuntu 22.04 LTS AMI
   - Select t3.medium instance
   - Configure security groups
   - Create or use existing key pair

2. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose git -y
   sudo usermod -aG docker ubuntu
   ```

4. **Deploy Application**
   ```bash
   git clone your-repository-url
   cd car-erp-system
   cp env.example .env
   # Edit .env file with production settings
   sudo docker-compose up -d
   ```

### Option 3: Google Cloud Platform

#### Server Requirements
- **Machine Type**: e2-medium or larger
- **Boot Disk**: 30GB+ SSD
- **Firewall**: HTTP, HTTPS, SSH
- **Cost**: $25-50/month

#### Deployment Steps

1. **Create GCP Project**
   ```bash
   # Visit: https://console.cloud.google.com/
   # Create new project
   ```

2. **Launch Compute Engine Instance**
   - Choose Ubuntu 22.04 LTS
   - Select e2-medium machine type
   - Configure firewall rules

3. **Deploy Application**
   ```bash
   ssh your-instance-ip
   # Follow similar steps as AWS/DigitalOcean
   ```

## 🔧 Production Configuration

### Environment Variables (.env)

```env
# Production Settings
DEBUG=False
SECRET_KEY=your-super-secure-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# Database (Production PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=car_erp_production
DB_USER=car_erp_user
DB_PASSWORD=your-secure-database-password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# Email Settings (Production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis (Production)
REDIS_URL=redis://localhost:6379/0

# File Upload Settings
MAX_UPLOAD_SIZE=10485760
MEDIA_ROOT=/app/media/
MEDIA_URL=/media/

# Admin Account
ADMIN_EMAIL=admin@your-domain.com
ADMIN_PASSWORD=your-secure-admin-password
```

### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: car_erp_production
      POSTGRES_USER: car_erp_user
      POSTGRES_PASSWORD: your-secure-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  backend:
    build: ./car_erp_backend
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn car_erp_backend.wsgi:application --bind 0.0.0.0:8000"
    volumes:
      - ./car_erp_backend:/app
      - media_volume:/app/media
      - static_volume:/app/staticfiles
    environment:
      - DEBUG=False
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped

  frontend:
    build: ./frontend
    command: npm run build && npx serve -s build -l 3000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - static_volume:/var/www/static
      - media_volume:/var/www/media
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  media_volume:
  static_volume:
```

## 🔒 SSL Certificate Setup

### Using Let's Encrypt (Free)

1. **Install Certbot**
   ```bash
   apt install certbot python3-certbot-nginx -y
   ```

2. **Get SSL Certificate**
   ```bash
   certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

3. **Auto-renewal**
   ```bash
   crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet
   ```

## 🌐 Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name your-domain.com www.your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com www.your-domain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /media/ {
            alias /var/www/media/;
        }

        location /static/ {
            alias /var/www/static/;
        }

        location /admin/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## 📊 Monitoring & Maintenance

### 1. System Monitoring

Install monitoring tools:
```bash
# Install htop for system monitoring
apt install htop -y

# Install Docker monitoring
docker stats

# Check logs
docker-compose logs -f
```

### 2. Database Backups

Create backup script `backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec db pg_dump -U car_erp_user car_erp_production > backup_$DATE.sql
```

### 3. Log Management

```bash
# View application logs
docker-compose logs backend
docker-compose logs frontend

# Rotate logs
docker system prune -f
```

## 🔄 Deployment Automation

### GitHub Actions (CI/CD)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Server

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /path/to/your/project
          git pull origin main
          docker-compose -f docker-compose.prod.yml down
          docker-compose -f docker-compose.prod.yml up -d --build
```

## 💰 Cost Estimation

### Monthly Costs by Provider

| Provider | Plan | RAM | Storage | Cost/Month |
|----------|------|-----|---------|------------|
| DigitalOcean | Basic | 4GB | 80GB | $24 |
| AWS EC2 | t3.medium | 4GB | 30GB | $30 |
| Google Cloud | e2-medium | 4GB | 30GB | $25 |
| Linode | Nanode | 4GB | 80GB | $20 |
| Vultr | Cloud Compute | 4GB | 80GB | $24 |

### Additional Costs
- **Domain Name**: $10-15/year
- **SSL Certificate**: Free (Let's Encrypt)
- **Email Service**: $5-10/month (optional)
- **Backup Storage**: $5-10/month

## 🚨 Security Checklist

### Server Security
- [ ] Update system packages regularly
- [ ] Configure firewall (UFW)
- [ ] Use SSH keys instead of passwords
- [ ] Disable root login
- [ ] Install fail2ban
- [ ] Regular security updates

### Application Security
- [ ] Use strong passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Regular database backups
- [ ] Monitor application logs
- [ ] Update dependencies regularly

### Database Security
- [ ] Use strong database passwords
- [ ] Restrict database access
- [ ] Regular backups
- [ ] Monitor database logs

## 📞 Support & Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   sudo netstat -tlnp | grep :80
   sudo kill -9 PID
   ```

2. **Docker Permission Issues**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

3. **SSL Certificate Issues**
   ```bash
   certbot renew --dry-run
   ```

4. **Database Connection Issues**
   ```bash
   docker-compose exec db psql -U car_erp_user -d car_erp_production
   ```

### Performance Optimization

1. **Enable Gzip Compression**
2. **Use CDN for Static Files**
3. **Database Query Optimization**
4. **Caching with Redis**
5. **Load Balancing (for high traffic)**

---

## 🎯 Quick Start Commands

```bash
# 1. Connect to server
ssh root@your-server-ip

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# 3. Clone project
git clone your-repository-url
cd car-erp-system

# 4. Configure environment
cp env.example .env
nano .env  # Edit with production settings

# 5. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 6. Setup SSL
certbot --nginx -d your-domain.com

# 7. Check status
docker-compose ps
```

Your Car ERP System will be accessible at `https://your-domain.com`!

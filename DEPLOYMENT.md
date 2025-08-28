# Deployment Guide

This guide covers deployment options for the Travel Booking Application.

## 🐍 PythonAnywhere Deployment

### Step 1: Upload Code
1. Create a PythonAnywhere account
2. Upload your code via Git or file upload
3. Extract to `/home/yourusername/travel_booking`

### Step 2: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 travel_booking
pip install -r requirements.txt
```

### Step 3: Configure Database
1. Go to "Databases" tab in PythonAnywhere dashboard
2. Create a new MySQL database
3. Note the database name, username, and password

### Step 4: Update Settings
Create `.env` file with production settings:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com

DB_ENGINE=django.db.backends.mysql
DB_NAME=yourusername$travel_booking
DB_USER=yourusername
DB_PASSWORD=your-db-password
DB_HOST=yourusername.mysql.pythonanywhere-services.com
```

### Step 5: Configure Web App
1. Go to "Web" tab
2. Create new web app
3. Choose "Manual configuration" with Python 3.10
4. Set source code path: `/home/yourusername/travel_booking`
5. Set virtualenv path: `/home/yourusername/.virtualenvs/travel_booking`

### Step 6: Configure WSGI
Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import os
import sys

path = '/home/yourusername/travel_booking'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'travel_booking.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 7: Setup Database
```bash
cd ~/travel_booking
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### Step 8: Configure Static Files
In web app configuration:
- URL: `/static/`
- Directory: `/home/yourusername/travel_booking/staticfiles/`

## ☁️ AWS Deployment

### Prerequisites
- AWS account
- Domain name (optional)
- Basic knowledge of AWS services

### Step 1: Launch EC2 Instance
1. Launch Ubuntu 20.04 LTS instance
2. Configure security groups (HTTP, HTTPS, SSH)
3. Create and download key pair

### Step 2: Connect and Setup Server
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx mysql-server -y

# Install additional packages
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
```

### Step 3: Clone and Setup Application
```bash
cd /home/ubuntu
git clone your-repo-url travel_booking
cd travel_booking

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

### Step 4: Configure MySQL
```bash
sudo mysql
```
```sql
CREATE DATABASE travel_booking_db;
CREATE USER 'travel_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON travel_booking_db.* TO 'travel_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 5: Configure Environment
Create `/home/ubuntu/travel_booking/.env`:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-ip

DB_ENGINE=django.db.backends.mysql
DB_NAME=travel_booking_db
DB_USER=travel_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=3306
```

### Step 6: Setup Django
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### Step 7: Configure Gunicorn
Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/travel_booking
ExecStart=/home/ubuntu/travel_booking/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/travel_booking/travel_booking.sock travel_booking.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start Gunicorn:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Step 8: Configure Nginx
Create `/etc/nginx/sites-available/travel_booking`:
```nginx
server {
    listen 80;
    server_name your-domain.com your-ec2-ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/travel_booking;
    }
    
    location /media/ {
        root /home/ubuntu/travel_booking;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/travel_booking/travel_booking.sock;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/travel_booking /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Configure SSL (Optional)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "travel_booking.wsgi:application"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DB_HOST=db
    depends_on:
      - db
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: travel_booking_db
      MYSQL_USER: travel_user
      MYSQL_PASSWORD: secure_password
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - mysql_data:/var/lib/mysql

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  mysql_data:
  static_volume:
  media_volume:
```

### Deploy with Docker
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

## 🔧 Production Checklist

### Security
- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up SSL certificate
- [ ] Configure firewall
- [ ] Regular security updates

### Performance
- [ ] Configure caching (Redis/Memcached)
- [ ] Set up CDN for static files
- [ ] Database optimization
- [ ] Enable gzip compression
- [ ] Monitor application performance

### Monitoring
- [ ] Set up logging
- [ ] Configure error tracking (Sentry)
- [ ] Database backups
- [ ] Health checks
- [ ] Uptime monitoring

### Maintenance
- [ ] Automated deployments
- [ ] Database migrations strategy
- [ ] Backup and recovery plan
- [ ] Documentation updates
- [ ] Regular dependency updates

## 📊 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `example.com,www.example.com` |
| `DB_ENGINE` | Database engine | `django.db.backends.mysql` |
| `DB_NAME` | Database name | `travel_booking_db` |
| `DB_USER` | Database user | `travel_user` |
| `DB_PASSWORD` | Database password | `secure_password` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `3306` |

## 🆘 Troubleshooting

### Common Issues

**Database Connection Error**
- Check database credentials
- Ensure database server is running
- Verify network connectivity

**Static Files Not Loading**
- Run `python manage.py collectstatic`
- Check static files configuration
- Verify web server static file serving

**Permission Denied**
- Check file permissions
- Ensure correct user ownership
- Verify directory permissions

**Import Errors**
- Activate virtual environment
- Install all requirements
- Check Python path configuration

### Logs Location
- **PythonAnywhere**: Check error logs in dashboard
- **AWS**: `/var/log/nginx/` and `journalctl -u gunicorn`
- **Docker**: `docker-compose logs`

## 📞 Support

For deployment issues:
1. Check the logs first
2. Verify configuration files
3. Test database connectivity
4. Review security group settings (AWS)
5. Contact platform support if needed

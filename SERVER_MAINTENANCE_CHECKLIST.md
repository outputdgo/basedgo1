# Django Server Maintenance Checklist

## Quick Server Health Check (Weekly)

### 1. Basic Service Status
```bash
# Check if all services are running
sudo systemctl status nginx
sudo systemctl status gunicorn
sudo systemctl status fail2ban

# Quick process check
ps aux | grep -E "(nginx|gunicorn)" | grep -v grep
```

### 2. Server Resources
```bash
# Check disk space (should be < 80%)
df -h

# Check memory usage
free -h

# Check CPU usage
top -n 1 | head -10
```

### 3. Log Review
```bash
# Check for errors in the last 24 hours
sudo journalctl -u nginx --since "24 hours ago" | grep -i error
sudo journalctl -u gunicorn --since "24 hours ago" | grep -i error

# Django error logs
tail -50 /var/log/django/django.log | grep -i error
```

## Security Monitoring (Bi-weekly)

### 1. Failed Login Attempts
```bash
# Check fail2ban status
sudo fail2ban-client status
sudo fail2ban-client status nginx-limit-req

# Review auth logs for suspicious activity
sudo grep "Failed password" /var/log/auth.log | tail -20
```

### 2. SSL Certificate Status
```bash
# Check certificate expiration (should be > 30 days)
sudo certbot certificates

# Test SSL configuration
curl -I https://outputdgo.com | head -5
```

### 3. Firewall Status
```bash
# Verify firewall rules
sudo ufw status verbose

# Check open ports
sudo netstat -tulpn | grep LISTEN
```

## Application Maintenance (Monthly)

### 1. Django Updates
```bash
# Activate virtual environment
source venv312/bin/activate

# Check for outdated packages
pip list --outdated

# Update Django (test first!)
# pip install --upgrade django

# Run migrations if any
python manage.py makemigrations
python manage.py migrate
```

### 2. Database Maintenance
```bash
# Database backup (already automated via cron)
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Check database size
du -sh *.sqlite3
```

### 3. Static Files & Media
```bash
# Collect static files after updates
python manage.py collectstatic --noinput

# Clean old log files (older than 30 days)
find /var/log/django/ -name "*.log" -mtime +30 -delete
```

## Performance Optimization (Quarterly)

### 1. Server Performance
```bash
# Analyze nginx access logs for top pages
awk '{print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -10

# Check response times
tail -1000 /var/log/nginx/access.log | awk '{print $NF}' | sort -n | tail -10
```

### 2. Database Optimization
```bash
# Run Django's database optimization
python manage.py optimize_db  # If you have this command

# Check for unused migrations
python manage.py showmigrations
```

## Backup Verification (Monthly)

### 1. Automated Backups
```bash
# Verify backup script is running
crontab -l | grep backup

# Check backup files exist and are recent
ls -la /home/ubuntu/backups/ | head -10

# Test backup restoration (on test environment)
```

### 2. Configuration Backups
```bash
# Backup important config files
sudo cp /etc/nginx/sites-available/outputdgo.com /home/ubuntu/backups/nginx_config_$(date +%Y%m%d).conf
sudo cp /etc/systemd/system/gunicorn.service /home/ubuntu/backups/gunicorn_service_$(date +%Y%m%d).service
```

## Troubleshooting Quick Reference

### Common Issues & Solutions

#### 1. Site Not Loading
```bash
# Check nginx status and restart if needed
sudo systemctl status nginx
sudo systemctl restart nginx

# Check gunicorn status
sudo systemctl status gunicorn
sudo systemctl restart gunicorn

# Check logs for errors
sudo tail -50 /var/log/nginx/error.log
```

#### 2. 502 Bad Gateway
```bash
# Usually gunicorn issue
sudo systemctl restart gunicorn
sudo journalctl -u gunicorn -f

# Check socket file
ls -la /run/gunicorn.sock
```

#### 3. SSL Certificate Issues
```bash
# Renew certificates
sudo certbot renew --dry-run
sudo certbot renew

# Restart nginx after renewal
sudo systemctl reload nginx
```

#### 4. High Memory/CPU Usage
```bash
# Identify resource-heavy processes
top -o %MEM
top -o %CPU

# Restart services if needed
sudo systemctl restart gunicorn
```

#### 5. Email Not Working
```bash
# Test email configuration
cd /home/ubuntu/basedgo1
source venv312/bin/activate
python cf_test.py

# Check Django email settings
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'admin@outputdgo.com', ['your-email@example.com'])
```

## Security Maintenance Scripts

### Available Scripts
- `./security-hardening.sh` - Full security hardening
- `./ssl-setup.sh` - SSL certificate management
- `./security-monitor.sh` - Security monitoring
- `./backup.sh` - Database and file backup
- `./deploy.sh` - Safe deployment
- `./restart-server.sh` - Service restart

### When to Run
- **security-hardening.sh**: After OS updates or security concerns
- **ssl-setup.sh**: When certificates need renewal
- **security-monitor.sh**: Weekly for security review
- **backup.sh**: Already automated via cron (daily)
- **deploy.sh**: When deploying code changes
- **restart-server.sh**: When configuration changes are made

## Environment Activation

```bash
# Always activate virtual environment before Django commands
cd /home/ubuntu/basedgo1
source venv312/bin/activate

# Verify you're in the right environment
which python
python --version  # Should be 3.12.x
```

## Emergency Contacts & Resources

### Key File Locations
- **Django Project**: `/home/ubuntu/basedgo1/`
- **Nginx Config**: `/etc/nginx/sites-available/outputdgo.com`
- **Gunicorn Service**: `/etc/systemd/system/gunicorn.service`
- **SSL Certificates**: `/etc/letsencrypt/live/outputdgo.com/`
- **Logs**: `/var/log/nginx/` and `/var/log/django/`
- **Backups**: `/home/ubuntu/backups/`

### Important Commands
```bash
# Quick server restart
./restart-server.sh

# Safe deployment
./deploy.sh

# Emergency stop all services
sudo systemctl stop nginx gunicorn

# Emergency start all services
sudo systemctl start gunicorn nginx
```

## Notes Section
_Use this space to track any custom modifications or issues you encounter:_

- 
- 
- 

---
**Last Updated**: $(date)
**Server**: outputdgo.com
**Django Version**: 5.2.3
**Python Version**: 3.12.x

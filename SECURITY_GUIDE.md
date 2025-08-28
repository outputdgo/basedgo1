# 🔐 Security Hardening Guide for basedgo1

## Overview
This guide provides comprehensive security hardening for your Django production server. The security vulnerabilities identified and their solutions are documented below.

## 🚨 Critical Vulnerabilities Identified

### 1. **No HTTPS/SSL Encryption**
- **Risk**: All traffic between users and server is unencrypted
- **Impact**: Passwords, session tokens, and sensitive data can be intercepted
- **Solution**: Implement SSL/TLS with Let's Encrypt

### 2. **No Rate Limiting**
- **Risk**: Vulnerable to brute force attacks and DDoS
- **Impact**: Server can be overwhelmed or accounts compromised
- **Solution**: Nginx rate limiting zones implemented

### 3. **No Intrusion Prevention**
- **Risk**: No protection against repeated failed login attempts
- **Impact**: Brute force attacks can succeed
- **Solution**: Fail2Ban with custom rules

### 4. **Exposed Admin Panel**
- **Risk**: Default `/admin/` URL is easily discoverable
- **Impact**: Increases attack surface for admin panel
- **Solution**: Custom admin URL obfuscation

### 5. **Missing Security Headers**
- **Risk**: XSS, clickjacking, and other client-side attacks
- **Impact**: User data can be compromised
- **Solution**: Comprehensive security headers

## 🛠️ Security Hardening Implementation

### Phase 1: System Hardening
```bash
# Run the main security hardening script
sudo bash security-hardening.sh
```

**What this does:**
- Installs and configures UFW firewall
- Sets up Fail2Ban with custom rules
- Configures automatic security updates
- Hardens kernel parameters
- Sets secure file permissions
- Configures log rotation

### Phase 2: SSL/HTTPS Setup
```bash
# Replace 'yourdomain.com' with your actual domain
sudo bash ssl-setup.sh yourdomain.com
```

**What this does:**
- Installs Let's Encrypt certificates
- Configures Nginx with enhanced security headers
- Sets up automatic certificate renewal
- Implements rate limiting
- Blocks malicious bots and attack patterns

### Phase 3: Django Security Enhancement
1. Update your Django settings with enhanced security:
```bash
# Merge SECURITY_SETTINGS.py into your settings_production.py
cat SECURITY_SETTINGS.py >> base/settings_production.py
```

2. Update your main URLs to use custom admin URL:
```python
# In base/urls.py, change:
# path('admin/', admin.site.urls),
# to:
path(settings.ADMIN_URL, admin.site.urls),
```

### Phase 4: Monitoring Setup
```bash
# Make monitoring script executable
chmod +x security-monitor.sh

# Set up monitoring cron job (runs every 5 minutes)
echo "*/5 * * * * /home/ubuntu/basedgo1/security-monitor.sh" | sudo crontab -
```

## 🔧 Additional Security Configurations

### Environment Variables
Create a `.env` file for sensitive settings:
```bash
# Database and security settings
SECRET_KEY=your-very-long-secret-key-here
DEBUG=False
DJANGO_ADMIN_URL=your-custom-admin-url-123/
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL=admin@yourdomain.com
```

### Firewall Rules
```bash
# Check firewall status
sudo ufw status

# View active rules
sudo ufw numbered
```

### Fail2Ban Status
```bash
# Check Fail2Ban status
sudo fail2ban-client status

# Check specific jail
sudo fail2ban-client status nginx-http-auth
```

## 📊 Security Monitoring

### Log Files to Monitor
- `/var/log/nginx/access.log` - Web traffic
- `/var/log/nginx/error.log` - Nginx errors
- `/var/log/auth.log` - Authentication attempts
- `/home/ubuntu/basedgo1/security.log` - Django security events
- `/home/ubuntu/basedgo1/security-monitor.log` - Monitoring alerts

### Security Alerts
The monitoring script will email alerts for:
- Failed login attempts (>10 in 5 minutes)
- 404 scanning attempts (>50 in 5 minutes)
- High disk usage (>85%)
- Service failures
- High network connections (>100 concurrent)
- SSL certificate expiry (7 days warning)

## 🔍 Security Checklist

### Before Going Live:
- [ ] Run security-hardening.sh
- [ ] Set up SSL with ssl-setup.sh
- [ ] Update Django settings with security enhancements
- [ ] Change admin URL from default
- [ ] Set up monitoring and alerts
- [ ] Configure email notifications
- [ ] Test all functionality with HTTPS
- [ ] Verify firewall rules
- [ ] Check Fail2Ban configuration

### Regular Maintenance:
- [ ] Monitor security logs weekly
- [ ] Update system packages monthly
- [ ] Review firewall logs
- [ ] Check SSL certificate status
- [ ] Backup database regularly
- [ ] Review user accounts and permissions

## 🚨 Security Incident Response

### If You Detect an Attack:
1. **Check logs immediately:**
   ```bash
   sudo tail -f /var/log/nginx/access.log | grep -E "(404|500|403)"
   sudo fail2ban-client status
   ```

2. **Block specific IPs if needed:**
   ```bash
   sudo ufw insert 1 deny from ATTACKER_IP
   ```

3. **Review Django security logs:**
   ```bash
   tail -f /home/ubuntu/basedgo1/security.log
   ```

## 🔐 Password Security

### For Django Admin:
- Use strong passwords (12+ characters)
- Enable two-factor authentication if possible
- Regularly rotate admin passwords
- Use unique passwords for each admin user

### For Server Access:
- Use SSH keys instead of passwords
- Disable password authentication in SSH
- Use strong passphrases for SSH keys

## 📈 Performance vs Security

### Current Configuration Balance:
- **Rate Limiting**: Balanced to allow normal usage while blocking attacks
- **SSL/TLS**: Modern ciphers for security without breaking compatibility
- **Headers**: Comprehensive security headers that don't break functionality
- **Monitoring**: Real-time monitoring without performance impact

### Tuning Options:
- Adjust rate limits in Nginx configuration
- Modify Fail2Ban ban times and thresholds
- Update CSP headers as your application evolves

## 🆘 Emergency Procedures

### If Site Goes Down:
1. Check service status: `sudo systemctl status nginx gunicorn`
2. Check logs: `sudo journalctl -u nginx -f`
3. Restart services: `sudo systemctl restart nginx gunicorn`
4. Check SSL certificates: `sudo certbot certificates`

### If Under Attack:
1. Enable strict rate limiting temporarily
2. Block entire IP ranges if needed
3. Enable maintenance mode
4. Contact hosting provider if DDoS

## 📞 Support and Updates

### Keep Updated:
- Security patches are automatically installed
- Monitor Django security releases
- Update fail2ban rules as needed
- Review and update firewall rules quarterly

Remember: Security is an ongoing process, not a one-time setup. Regular monitoring and updates are essential for maintaining a secure environment.

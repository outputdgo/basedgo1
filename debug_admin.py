#!/usr/bin/env python3
"""
Django Admin Session Debugger
Run this script to check and fix common admin session issues
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.insert(0, '/home/ubuntu/basedgo1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def check_admin_sessions():
    print("=" * 50)
    print("DJANGO ADMIN SESSION DEBUGGER")
    print("=" * 50)
    
    # Check session configuration
    print(f"DEBUG: {settings.DEBUG}")
    print(f"SESSION_COOKIE_DOMAIN: {getattr(settings, 'SESSION_COOKIE_DOMAIN', 'Not set')}")
    print(f"SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', 'Not set')}")
    print(f"SESSION_COOKIE_SAMESITE: {getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Not set')}")
    print(f"SESSION_COOKIE_AGE: {getattr(settings, 'SESSION_COOKIE_AGE', 'Not set')}")
    print(f"CSRF_COOKIE_DOMAIN: {getattr(settings, 'CSRF_COOKIE_DOMAIN', 'Not set')}")
    print(f"CSRF_TRUSTED_ORIGINS: {getattr(settings, 'CSRF_TRUSTED_ORIGINS', 'Not set')}")
    print()
    
    # Check active sessions
    now = timezone.now()
    active_sessions = Session.objects.filter(expire_date__gt=now)
    expired_sessions = Session.objects.filter(expire_date__lte=now)
    
    print(f"Active sessions: {active_sessions.count()}")
    print(f"Expired sessions: {expired_sessions.count()}")
    
    # Check admin users
    admin_users = User.objects.filter(is_staff=True, is_active=True)
    superusers = User.objects.filter(is_superuser=True, is_active=True)
    
    print(f"Active admin users: {admin_users.count()}")
    print(f"Active superusers: {superusers.count()}")
    
    if superusers.exists():
        print("\nSuperuser accounts:")
        for user in superusers:
            last_login = user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'Never'
            print(f"  - {user.username} (last login: {last_login})")
    
    print("\n" + "=" * 50)
    print("TROUBLESHOOTING TIPS:")
    print("=" * 50)
    print("1. Clear browser cookies for outputdgo.com")
    print("2. Try accessing admin in incognito/private browsing")
    print("3. Check if you're accessing via HTTP vs HTTPS")
    print("4. Admin URL: http://outputdgo.com/x8k9m2n5p7q1/")
    print("5. If issues persist, clear all sessions with: python manage.py clearsessions")

def clear_old_sessions():
    """Clear sessions older than 7 days"""
    cutoff = timezone.now() - timedelta(days=7)
    old_sessions = Session.objects.filter(expire_date__lte=cutoff)
    count = old_sessions.count()
    old_sessions.delete()
    print(f"Cleared {count} old sessions")

if __name__ == "__main__":
    try:
        check_admin_sessions()
        
        # Ask if user wants to clear old sessions
        response = input("\nDo you want to clear old sessions? (y/N): ").strip().lower()
        if response == 'y':
            clear_old_sessions()
            print("Old sessions cleared. Try logging into admin again.")
    
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you're running this from the correct directory.")

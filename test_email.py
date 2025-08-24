#!/usr/bin/env python3
"""
Email Configuration Test Script
Run this to test if your email settings are working properly.
Usage: python test_email.py recipient@example.com
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email(recipient_email):
    """Test email configuration by sending a test email."""
    print(f"Testing email configuration...")
    print(f"Email Host: {settings.EMAIL_HOST}")
    print(f"Email Port: {settings.EMAIL_PORT}")
    print(f"Email User: {settings.EMAIL_HOST_USER}")
    print(f"Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"Sending test email to: {recipient_email}")
    
    try:
        send_mail(
            subject='Test Email from outputdgo.com',
            message='This is a test email to verify your Django email configuration is working properly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Email failed to send: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_email.py recipient@example.com")
        sys.exit(1)
    
    recipient = sys.argv[1]
    success = test_email(recipient)
    sys.exit(0 if success else 1)

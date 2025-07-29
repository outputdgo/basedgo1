from .settings import *
import os
from decouple import config

# Production settings
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='yourdomain.com,www.yourdomain.com').split(',')

# Cloudflare CDN Configuration
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
ADMIN_URL = config('ADMIN_URL', default='admin/')


# Static files collection for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files served locally (cached by Cloudflare)
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cloudflare specific settings
SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', '{"scheme":"https"}')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Updated middleware with Cloudflare support
MIDDLEWARE = [
    'cloudflare_middleware.CloudflareMiddleware',
] + MIDDLEWARE  # Add Cloudflare middleware to existing middleware

# Database - use environment variables in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use environment variables for sensitive data
SECRET_KEY = config('DJANGO_SECRET_KEY')

# Email configuration for contact forms
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

# The config() function will automatically raise an error if the variable is not found

# Logging for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': config('LOG_LEVEL', default='INFO'),
            'propagate': True,
        },
    },
}
# AWS_ACCESS_KEY_ID = os.environ.get('OCI_ACCESS_KEY')
# AWS_SECRET_ACCESS_KEY = os.environ.get('OCI_SECRET_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('OCI_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.environ.get('OCI_REGION', 'us-ashburn-1')

from decouple import config
"""
Django settings for basedgo1 project.

This settings file adapts to both development and production environments
using environment variables from .env file.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment-based configuration
DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-development-key-change-me')

# Hosts configuration - adapts based on environment
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Admin URL (customizable for security)
ADMIN_URL = config('ADMIN_URL', default='admin/')

# Application definition
INSTALLED_APPS = [
    'home.apps.HomeConfig',
    'work.apps.WorkConfig',
    'outreach.apps.OutreachConfig',
    'contact.apps.ContactConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware - add Cloudflare middleware if needed
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add Cloudflare middleware in production - TESTING SIMPLIFIED SECURITY
if not DEBUG:
    MIDDLEWARE.insert(0, 'cloudflare_middleware.CloudflareMiddleware')
    MIDDLEWARE.insert(1, 'security_middleware.SecurityHeadersMiddleware')  # Simplified version

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings (production only)
if not DEBUG:
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
    SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=True, cast=bool)
    SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=bool)
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=0, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookie security (disable for HTTP, enable when you have HTTPS)
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
    
    # Session and cookie settings for Cloudflare compatibility - SIMPLIFIED
    SESSION_COOKIE_DOMAIN = config('SESSION_COOKIE_DOMAIN', default=None)
    CSRF_COOKIE_DOMAIN = config('CSRF_COOKIE_DOMAIN', default=None)
    SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE', default='Lax')
    CSRF_COOKIE_SAMESITE = config('CSRF_COOKIE_SAMESITE', default='Lax')
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = False  # Must be False for CSRF to work with AJAX
    SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', default=86400, cast=int)  # 24 hours
    SESSION_EXPIRE_AT_BROWSER_CLOSE = config('SESSION_EXPIRE_AT_BROWSER_CLOSE', default=False, cast=bool)
    # SESSION_SAVE_EVERY_REQUEST = config('SESSION_SAVE_EVERY_REQUEST', default=False, cast=bool)  # Commented out
    
    # CSRF settings for better compatibility
    CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='https://outputdgo.com,https://www.outputdgo.com').split(',')
    CSRF_USE_SESSIONS = config('CSRF_USE_SESSIONS', default=False, cast=bool)
    
    # Additional security headers
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
    
    # Content Security Policy (CSP)
    CSP_DEFAULT_SRC = config('CSP_DEFAULT_SRC', default="'self'")
    CSP_SCRIPT_SRC = config('CSP_SCRIPT_SRC', default="'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com")
    CSP_STYLE_SRC = config('CSP_STYLE_SRC', default="'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com")
    CSP_FONT_SRC = config('CSP_FONT_SRC', default="'self' https://fonts.gstatic.com https://cdn.jsdelivr.net")
    CSP_IMG_SRC = config('CSP_IMG_SRC', default="'self' data: https: blob:")
    CSP_CONNECT_SRC = config('CSP_CONNECT_SRC', default="'self'")
    CSP_FRAME_SRC = config('CSP_FRAME_SRC', default="'none'")
    CSP_OBJECT_SRC = config('CSP_OBJECT_SRC', default="'none'")
    CSP_BASE_URI = config('CSP_BASE_URI', default="'self'")
    CSP_FORM_ACTION = config('CSP_FORM_ACTION', default="'self'")
    
    # Permissions Policy
    PERMISSIONS_POLICY = {
        'accelerometer': '()',
        'ambient-light-sensor': '()',
        'autoplay': '()',
        'battery': '()',
        'camera': '()',
        'cross-origin-isolated': '()',
        'display-capture': '()',
        'document-domain': '()',
        'encrypted-media': '()',
        'execution-while-not-rendered': '()',
        'execution-while-out-of-viewport': '()',
        'fullscreen': '(self)',
        'geolocation': '()',
        'gyroscope': '()',
        'keyboard-map': '()',
        'magnetometer': '()',
        'microphone': '()',
        'midi': '()',
        'navigation-override': '()',
        'payment': '()',
        'picture-in-picture': '()',
        'publickey-credentials-get': '()',
        'screen-wake-lock': '()',
        'sync-xhr': '(self)',
        'usb': '()',
        'web-share': '()',
        'xr-spatial-tracking': '()',
    }
    
    # Cloudflare specific settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', '{"scheme":"https"}')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

# Logging configuration
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
            'level': 'INFO' if DEBUG else 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'] if DEBUG else ['file', 'console'],
            'level': config('LOG_LEVEL', default='INFO'),
            'propagate': True,
        },
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

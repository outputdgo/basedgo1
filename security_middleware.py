"""
Security Headers Middleware for Django
Adds Content Security Policy (CSP) and Permissions Policy headers
"""

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers including CSP and Permissions Policy
    """
    
    def process_response(self, request, response):
        # Only add headers in production (when DEBUG=False)
        if not settings.DEBUG:
            # Basic security headers
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['X-XSS-Protection'] = '1; mode=block'
            response['Referrer-Policy'] = 'same-origin'
            
            # Simple, safe CSP that won't cause hanging issues
            csp_policy = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://use.typekit.net https://p.typekit.net; "
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net https://use.typekit.net https://p.typekit.net; "
                "img-src 'self' data: https: blob:; "
                "connect-src 'self'; "
                "frame-src 'none'; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            )
            response['Content-Security-Policy'] = csp_policy
            
            # Basic Permissions Policy (safe subset)
            permissions_policy = (
                "accelerometer=(), "
                "camera=(), "
                "geolocation=(), "
                "microphone=(), "
                "payment=(), "
                "usb=(), "
                "fullscreen=(self)"
            )
            response['Permissions-Policy'] = permissions_policy
            
            # Remove server information
            if 'Server' in response:
                del response['Server']
        
        return response

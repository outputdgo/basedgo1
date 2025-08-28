"""
Security middleware for file uploads and media serving
"""
from django.http import HttpResponse

class MediaSecurityMiddleware:
    """
    Add security headers for media files
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers for media files
        if request.path.startswith('/media/'):
            # Prevent execution of uploaded files
            response['X-Content-Type-Options'] = 'nosniff'
            response['Content-Disposition'] = 'inline'
            
            # Prevent caching of potentially sensitive uploads
            if 'uploads/' in request.path:
                response['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
        
        return response

# cloudflare_middleware.py
class CloudflareMiddleware:
    """
    Middleware to handle Cloudflare headers and caching
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add cache headers for static content
        if request.path.startswith('/static/'):
            response['Cache-Control'] = 'max-age=31536000, public, immutable'
        elif request.path.startswith('/media/'):
            response['Cache-Control'] = 'max-age=2592000, public'
        
        # Handle Cloudflare real IP
        if 'HTTP_CF_CONNECTING_IP' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_CF_CONNECTING_IP']
        
        return response

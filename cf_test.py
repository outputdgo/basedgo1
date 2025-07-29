# Add this to home/views.py or create a separate file
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

@never_cache
def cloudflare_test(request):
    """Test endpoint to check Cloudflare connectivity"""
    cf_data = {
        'cloudflare_connected': bool(request.META.get('HTTP_CF_RAY')),
        'cf_ray': request.META.get('HTTP_CF_RAY', 'Not found'),
        'cf_connecting_ip': request.META.get('HTTP_CF_CONNECTING_IP', 'Not found'),
        'cf_visitor': request.META.get('HTTP_CF_VISITOR', 'Not found'),
        'cf_country': request.META.get('HTTP_CF_IPCOUNTRY', 'Not found'),
        'user_ip': request.META.get('REMOTE_ADDR', 'Unknown'),
        'ssl_header': request.META.get('HTTP_CF_VISITOR', 'Not using HTTPS'),
    }
    return JsonResponse(cf_data, json_dumps_params={'indent': 2})

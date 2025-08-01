from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.utils import timezone
import json

def session_debug(request):
    """Debug endpoint to check session and cookie information"""
    
    # Get session information
    session_key = request.session.session_key
    session_data = dict(request.session.items()) if request.session else {}
    
    # Get cookie information
    cookies = {}
    for name, value in request.COOKIES.items():
        cookies[name] = value
    
    # Get user information
    user_info = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None,
        'is_staff': request.user.is_staff if request.user.is_authenticated else False,
        'is_superuser': request.user.is_superuser if request.user.is_authenticated else False,
    }
    
    # Get request headers
    headers = {}
    for key, value in request.META.items():
        if key.startswith('HTTP_'):
            headers[key[5:].replace('_', '-').title()] = value
    
    debug_info = {
        'session': {
            'session_key': session_key,
            'session_data': session_data,
            'session_modified': request.session.modified if hasattr(request.session, 'modified') else None,
        },
        'cookies': cookies,
        'user': user_info,
        'request_info': {
            'method': request.method,
            'path': request.path,
            'is_secure': request.is_secure(),
            'host': request.get_host(),
        },
        'headers': headers,
        'csrf_token': request.META.get('CSRF_COOKIE', 'Not found'),
    }
    
    return JsonResponse(debug_info, indent=2)

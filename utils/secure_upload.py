import os
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from django.urls import reverse
from utils.file_validators import validate_image_upload, sanitize_filename
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@staff_member_required
def secure_ckeditor_upload(request):
    """
    Secure file upload handler for CKEditor with comprehensive validation
    """
    if request.method != 'POST':
        return JsonResponse({'error': {'message': 'Only POST method allowed'}}, status=405)
    
    if 'upload' not in request.FILES:
        return JsonResponse({'error': {'message': 'No file uploaded'}}, status=400)
    
    uploaded_file = request.FILES['upload']
    
    try:
        # Validate the uploaded file
        validate_image_upload(uploaded_file)
        
        # Sanitize filename and add UUID to prevent conflicts
        original_filename = sanitize_filename(uploaded_file.name)
        name, ext = os.path.splitext(original_filename)
        unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        
        # Save file securely
        upload_path = os.path.join(settings.CKEDITOR_UPLOAD_PATH, unique_filename)
        saved_path = default_storage.save(upload_path, uploaded_file)
        
        # Build URL for the uploaded file
        file_url = default_storage.url(saved_path)
        
        logger.info(f"Secure file upload successful: {unique_filename} by user {request.user.username}")
        
        # Return CKEditor-compatible response
        return JsonResponse({
            'url': file_url,
            'uploaded': True,
            'fileName': unique_filename
        })
        
    except Exception as e:
        logger.warning(f"File upload blocked: {str(e)} - File: {uploaded_file.name} - User: {request.user.username}")
        return JsonResponse({
            'error': {
                'message': str(e)
            }
        }, status=400)

@staff_member_required
def secure_ckeditor_browse(request):
    """
    Secure file browser for CKEditor (optional - can be disabled)
    """
    # For security, we'll return an empty list - disable browsing
    return JsonResponse({
        'currentFolder': {'path': '/', 'url': '/media/uploads/'},
        'files': [],
        'folders': []
    })

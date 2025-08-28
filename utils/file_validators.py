import os
import uuid
import magic
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def validate_image_upload(file):
    """
    Comprehensive image upload validation for security
    """
    # File size validation (5MB max)
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError(f'File too large. Maximum size is {max_size // (1024*1024)}MB.')
    
    # File extension validation
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in allowed_extensions:
        raise ValidationError(f'Invalid file extension. Allowed: {", ".join(allowed_extensions)}')
    
    # MIME type validation using python-magic
    try:
        file.seek(0)
        file_content = file.read(1024)  # Read first 1KB for magic number detection
        file.seek(0)  # Reset file pointer
        
        mime_type = magic.from_buffer(file_content, mime=True)
        allowed_mime_types = [
            'image/jpeg', 'image/jpg', 'image/png', 
            'image/gif', 'image/webp'
        ]
        
        if mime_type not in allowed_mime_types:
            logger.warning(f"Blocked file upload - invalid MIME type: {mime_type} for file: {file.name}")
            raise ValidationError(f'Invalid file type. Detected: {mime_type}')
    
    except Exception as e:
        logger.error(f"Error validating file {file.name}: {str(e)}")
        raise ValidationError('Unable to validate file type.')
    
    # Image validation using Pillow
    try:
        file.seek(0)
        with Image.open(file) as img:
            # Verify it's a valid image
            img.verify()
            
            # Check image dimensions (prevent massive images)
            if img.width > 4000 or img.height > 4000:
                raise ValidationError('Image dimensions too large. Maximum: 4000x4000 pixels.')
            
            # Check for common image formats
            if img.format not in ['JPEG', 'PNG', 'GIF', 'WEBP']:
                raise ValidationError(f'Unsupported image format: {img.format}')
                
    except Exception as e:
        logger.warning(f"Failed image validation for {file.name}: {str(e)}")
        raise ValidationError('Invalid or corrupted image file.')
    
    finally:
        file.seek(0)  # Reset file pointer for actual upload
    
    return file

def sanitize_filename(filename):
    """
    Sanitize uploaded filename to prevent path traversal and generate unique names
    """
    # Remove directory separators
    filename = os.path.basename(filename)
    
    # Remove or replace dangerous characters
    dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # Limit filename length and add UUID for uniqueness
    name, ext = os.path.splitext(filename)
    if len(name) > 30:
        name = name[:30]
    
    # Add UUID to prevent conflicts and guessing
    unique_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}".lower()
    return unique_name

def get_filename(filename, request):
    """
    CKEditor filename generator function
    """
    return sanitize_filename(filename)

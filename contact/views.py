from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.utils import timezone
from datetime import timedelta
import logging
import re
from .models import ContactSubmission

# Set up logging for spam attempts
logger = logging.getLogger(__name__)

# Anti-spam configuration
SPAM_PATTERNS = [
    r'.*nib$',  # Names ending in 'nib' (common spam pattern)
    r'^(leenib|nikita|robertnib|simonnib|georgenib)$',  # Known spam names
    r'.*rocketdigitaltech.*',  # Spam email domains
    r'.*dgtlsolution.*',
    r'sdasddsdsdsdsds',  # Obvious spam emails
]

SPAM_EMAIL_DOMAINS = [
    'rocketdigitaltech.com',
    'dgtlsolution.com',
]

def is_spam_submission(name, email, message):
    """Check if submission appears to be spam based on patterns"""
    
    # Check name patterns
    name_lower = name.lower().strip()
    for pattern in SPAM_PATTERNS:
        if re.match(pattern, name_lower, re.IGNORECASE):
            return True, f"Spam name pattern: {name}"
    
    # Check email patterns
    email_lower = email.lower().strip()
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, email_lower, re.IGNORECASE):
            return True, f"Spam email pattern: {email}"
    
    # Check for suspicious email domains
    email_domain = email_lower.split('@')[-1] if '@' in email_lower else ''
    if email_domain in SPAM_EMAIL_DOMAINS:
        return True, f"Spam email domain: {email_domain}"
    
    # Check for repeated submissions (same email in last hour)
    recent_cutoff = timezone.now() - timedelta(hours=1)
    recent_submissions = ContactSubmission.objects.filter(
        email=email,
        created_at__gte=recent_cutoff
    ).count()
    
    if recent_submissions >= 2:
        return True, f"Too many recent submissions from {email}"
    
    # Check message patterns (very short or very long messages are often spam)
    if len(message.strip()) < 10:
        return True, "Message too short"
    
    if len(message.strip()) > 500:
        return True, "Message too long"
    
    # Check for common spam words
    spam_words = ['seo', 'backlink', 'ranking', 'google top', 'increase traffic', 
                  'buy now', 'click here', 'make money', 'free offer']
    message_lower = message.lower()
    for word in spam_words:
        if word in message_lower:
            return True, f"Spam keyword detected: {word}"
    
    return False, None

# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        honeypot = request.POST.get("website", "")  # Our honeypot field
        form_timestamp = request.POST.get("form_timestamp", "")
        
        # Check honeypot - if filled, it's likely spam
        if honeypot:
            logger.warning(f"Spam attempt detected from {request.META.get('REMOTE_ADDR', 'unknown')} - honeypot filled: '{honeypot}'")
            # Return success to not tip off the bot, but don't save or process
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('success')
        
        # Time-based bot detection
        if form_timestamp:
            try:
                timestamp = int(form_timestamp)
                current_time = timezone.now().timestamp() * 1000  # Convert to milliseconds
                time_diff = (current_time - timestamp) / 1000  # Convert back to seconds
                
                # If submitted too quickly (less than 3 seconds) or timestamp is invalid
                if time_diff < 3:
                    logger.warning(f"Spam attempt detected from {request.META.get('REMOTE_ADDR', 'unknown')} - submitted too quickly: {time_diff:.2f}s")
                    messages.success(request, 'Your message has been sent successfully!')
                    return redirect('success')
                
                # If timestamp is way in the future or past (more than 1 hour)
                if time_diff > 3600 or time_diff < 0:
                    logger.warning(f"Spam attempt detected from {request.META.get('REMOTE_ADDR', 'unknown')} - invalid timestamp: {time_diff:.2f}s")
                    messages.success(request, 'Your message has been sent successfully!')
                    return redirect('success')
                    
            except (ValueError, TypeError):
                logger.warning(f"Spam attempt detected from {request.META.get('REMOTE_ADDR', 'unknown')} - invalid timestamp format")
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('success')
        
        # Additional validation
        if not name or not email or not message:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'contact/contact.html')
        
        # Advanced spam detection
        is_spam, spam_reason = is_spam_submission(name, email, message)
        if is_spam:
            logger.warning(f"Advanced spam detection triggered from {request.META.get('REMOTE_ADDR', 'unknown')} - {spam_reason} - Name: {name}, Email: {email}")
            # Return success to not tip off the bot, but don't save or process
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('success')
        
        # Save to database (only legitimate submissions reach this point)
        ContactSubmission.objects.create(
            name=name, 
            email=email, 
            message=message,
            honeypot=""  # Always empty for legitimate submissions
        )
        
        # Send email notification
        try:
            # Email to admin
            admin_subject = f"New Contact Form Submission from {name}"
            admin_message = f"""
New contact form submission received:

Name: {name}
Email: {email}
Message:
{message}

---
This email was sent automatically from outputdgo.com contact form.
            """
            
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMINS[0][1]],  # Send to admin email
                fail_silently=False,
            )
            
            # Confirmation email to user
            user_subject = "Thank you for contacting Output DGO"
            user_message = f"""
Hello {name},

Thank you for your message! We have received your contact form submission and will get back to you soon.

Your message:
{message}

Best regards,
The Output DGO team
            """
            
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,  # Don't fail if user email is invalid
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            
        except Exception as e:
            # Log the error but don't break the user experience
            print(f"Email sending failed: {e}")
            messages.success(request, 'Your message has been received!')
        
        return redirect('success')   
    return render(request, 'contact/contact.html')

def success(request):
    return render(request, 'contact/success.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import ContactSubmission

# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        # Save to database
        ContactSubmission.objects.create(name=name, email=email, message=message)
        
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
            user_subject = "Thank you for contacting outputdgo.com"
            user_message = f"""
Hello {name},

Thank you for your message! We have received your contact form submission and will get back to you soon.

Your message:
{message}

Best regards,
The outputdgo.com team
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

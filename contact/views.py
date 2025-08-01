from django.shortcuts import render, redirect
from .models import ContactSubmission

# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        ContactSubmission.objects.create(name=name, email=email, message=message)
        return redirect('success')   
    return render(request, 'contact/contact.html')

def success(request):
    return render(request, 'contact/success.html')

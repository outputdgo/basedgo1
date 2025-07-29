from django.contrib import admin
from .models import ContactSubmission

# Register your models here.
admin.site.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')
    list_filter = ('name',)
    ordering = ('-id',)
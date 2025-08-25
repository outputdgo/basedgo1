from django.db import models
from django.utils import timezone

# Create your models here.
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=600)
    # Honeypot field - should always be empty for legitimate submissions
    honeypot = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}  - {self.email}" 

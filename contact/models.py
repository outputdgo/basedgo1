from django.db import models

# Create your models here.
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=600)

    def __str__(self):
        return f"{self.name}  - {self.email}" 

from django.db import models
from work.models import Content, RandomSlugMixin
# Create your models here.

class OutreachPost(Content, RandomSlugMixin):
    body=models.TextField()


class OutreachImage(models.Model):
    outreach = models.ForeignKey(OutreachPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='outreach/images')
    caption = models.CharField(max_length=255, blank=True, null=True)

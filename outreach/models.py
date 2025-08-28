from django.db import models
from work.models import Content, RandomSlugMixin
from ckeditor_uploader.fields import RichTextUploadingField
from utils.file_validators import validate_image_upload
# Create your models here.

class OutreachPost(Content, RandomSlugMixin):
    body = RichTextUploadingField()


class OutreachImage(models.Model):
    outreach = models.ForeignKey(OutreachPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='outreach/images')
    caption = models.CharField(max_length=255, blank=True, null=True)

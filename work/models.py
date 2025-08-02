import random
import re
from django.db import models


class RandomSlugMixin:
    def save(self, *args, **kwargs):
        if not self.slug:
            ModelClass = self.__class__
            while True:
                random_slug = str(random.randint(100000, 999999))
                if not ModelClass.objects.filter(slug=random_slug).exists():
                    self.slug = random_slug
                    break
        super().save(*args, **kwargs)

# Create your models here.

class Content(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=False)
    updated = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    tags = models.CharField(max_length=100)

    
    def __str__(self):
        return self.title + ' - ' + self.description
    
    
    class Meta:
        abstract = True
    

class Project(Content, RandomSlugMixin):
    discipline = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='project/images')
    client = models.CharField(max_length=100)
    coverimage = models.ImageField(upload_to='project/images', blank=True, null=True)
    
    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project/images')
    description = models.CharField(max_length=100, blank=True, null=True)

class ProjectEmbeddedVideo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    video_url = models.URLField()
    description = models.CharField(max_length=100, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Convert YouTube watch URLs to embed URLs
        if 'youtube.com/watch?v=' in self.video_url:
            video_id = re.search(r'v=([^&]*)', self.video_url)
            if video_id:
                self.video_url = f'https://www.youtube.com/embed/{video_id.group(1)}'
        elif 'youtu.be/' in self.video_url:
            video_id = self.video_url.split('youtu.be/')[-1].split('?')[0]
            self.video_url = f'https://www.youtube.com/embed/{video_id}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Video for {self.project.title}"

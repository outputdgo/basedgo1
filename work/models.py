import random
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
    
    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project/images')
    description = models.CharField(max_length=100, blank=True, null=True)
    

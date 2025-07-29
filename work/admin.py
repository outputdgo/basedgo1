from django.contrib import admin
from .models import Project, ProjectImage

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectImage)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
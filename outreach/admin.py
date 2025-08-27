from django.contrib import admin
from .models import OutreachPost, OutreachImage
from ckeditor.widgets import CKEditorWidget
from django import forms

class OutreachPostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = OutreachPost
        fields = '__all__'

class OutreachPostAdmin(admin.ModelAdmin):
    form = OutreachPostAdminForm
    list_display = ['title', 'date', 'featured']
    list_filter = ['featured', 'date']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
admin.site.register(OutreachPost, OutreachPostAdmin)
admin.site.register(OutreachImage)

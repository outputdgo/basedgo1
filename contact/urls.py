from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='contactindex'),
    path('success/', views.success, name='success'),
]

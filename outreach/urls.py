from django.urls import path
from . import views

urlpatterns = [
    path("<int:outreachpost_id>/", views.detail, name="detail"),
    path("", views.index, name="outreachindex"),
]
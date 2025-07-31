from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views


urlpatterns = [
     path('', views.upload, name='upload'),
    
    path('delete_document/<int:pk>/', views.delete_document, name='delete_document'),
]

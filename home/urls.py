from django.contrib import admin
from django.urls import path,include
from home.views import *

app_name = 'home'
urlpatterns = [
    path('', index, name='index'),
    path('gallery', galleryView.as_view(), name="gallery"),
    path('search', search, name = "search"),
]

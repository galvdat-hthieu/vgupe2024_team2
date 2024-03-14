from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'main'
urlpatterns = [
    path('add_book/', add_book, name='add_book'),
]

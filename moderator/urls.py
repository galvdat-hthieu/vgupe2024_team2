from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'add_book'
urlpatterns = [
    path('', mod, name='mod'),
    path('add_book/', add_book, name='add_book'),
    path('save/', save, name='save'),
]

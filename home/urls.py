from django.contrib import admin
from django.urls import path,include
from home.views import *

app_name = 'main'
urlpatterns = [
    path('', index, name='index'),    
]

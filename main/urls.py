from django.contrib import admin
from django.urls import path,include
from main.views import *

app_name = 'main'
urlpatterns = [
    path('hi',index, name='index'),    
]

from django.contrib import admin
from django.urls import path, include
from user.views import *

app_name = 'user'
urlpatterns = [
    path('login',login, name='login'),   
]

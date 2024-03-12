from django.contrib import admin
from django.urls import path, include
from manager.views import *

app_name = 'manager'
urlpatterns = [
    path('account_manager',accountManager, name='index'),   
]
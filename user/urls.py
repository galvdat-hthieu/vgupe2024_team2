from django.contrib import admin
from django.urls import path, include
from user.views import *

app_name = 'user'
urlpatterns = [
    path('login/',loginView.as_view(), name='login'),
    path("info/", infoView.as_view(), name="info") 
]

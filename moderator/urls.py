from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "mod"
urlpatterns = [
    path("", modView.as_view(), name='mod'),
    path('addBook/', addBookView.as_view(), name='addBook'),
]

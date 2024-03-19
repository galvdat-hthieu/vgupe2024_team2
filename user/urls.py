from django.contrib import admin
from django.urls import path, include
from user.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'
urlpatterns = [
    path('login/',loginView.as_view(), name='login'),
    path("info/", infoView.as_view(), name="info")
]

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
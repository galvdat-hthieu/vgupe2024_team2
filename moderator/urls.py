from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "mod"
urlpatterns = [
    path("", modView.as_view(), name='mod'),
    path("addBook", addBookView.as_view(), name='addBook'),
    path('editBook/<int:id>', editBookView.as_view(), name='editBook'),
    path('addCopy/<int:id>', addCopyView.as_view(), name='addCopy'),
]

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
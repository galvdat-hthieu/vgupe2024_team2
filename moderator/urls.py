from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "mod"
urlpatterns = [
    path("", modView.as_view(), name='mod'),
    path('addBook/', addBookView.as_view(), name='addBook'),
    path('saveBook/', saveBookView.as_view(), name='saveBook'),
    path('addCopy/', addCopyView.as_view(), name='addCopy'),
    path('saveCopy/', saveCopyView.as_view(), name='saveCopy'),
]

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
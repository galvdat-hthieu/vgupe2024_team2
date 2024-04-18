from django.contrib import admin
from django.urls import path,include
from home.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'
urlpatterns = [
    path('', indexView.as_view(), name='index'),
    path("gallery", galleryView.as_view(), name="gallery"),
    path('gallery/bookid=<int:id>/detail',bookView.as_view(), name="book"),
    path('gallery/bookid=<int:id>/pdf', bookPDFView.as_view(), name="bookPDF"),
    path('shelf/userid=<int:id>',shelfView.as_view(), name = "shelf"),
    path('borrow',borrowView.as_view(), name = "borrow"),
]


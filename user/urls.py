from django.contrib import admin
from django.urls import path, include
from user.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'
urlpatterns = [
    path('login/', loginView.as_view(), name='login'),
    path('logout/', logoutView.as_view(), name='logout'),
    path("changePassword", changePasswordView.as_view(), name="changePassword"),
    path('register/', registerView.as_view(), name="register"),
    path("profile/info/", profileInfoView.as_view(), name="info"),
    path("profile/edit/", profileEditView.as_view(), name="edit"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
]

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
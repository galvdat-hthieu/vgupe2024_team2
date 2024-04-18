from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from control.views import *


app_name = 'control'
urlpatterns = [
    path('', ControlView.as_view(), name="control"),
    path('review/modApplication', ModApplyView.as_view(), name="reviewModApp"),
]

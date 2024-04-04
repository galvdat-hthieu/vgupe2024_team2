from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import signupRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('user/', include('user.urls')),
    # Moderator page
    path('mod/', include('moderator.urls')),
    path('accounts/social/signup/', signupRedirect.as_view()),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
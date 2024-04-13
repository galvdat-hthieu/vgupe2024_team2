from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from user.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'
urlpatterns = [
    path('register/', registerView.as_view(), name="register"),
    path('login/', loginView.as_view(), name='login'),
    path('logout/', logoutView.as_view(), name='logout'),
    path("password", changePasswordView.as_view(), name="changePassword"),

    path("recover", 
         auth_views.PasswordResetView.as_view(success_url=reverse_lazy("user:password_reset_done"),
                                              email_template_name = "user/password_reset_email.html",
                                              template_name = "user/password_reset_form.html",
                                              subject_template_name = "user/password_reset_subject.txt"
                                              ), name="reset_password"),
    path("recover/sent/", auth_views.PasswordResetDoneView.as_view(
                        template_name = "user/password_reset_done.html"
    ), name="password_reset_done"),
    path("recover/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy("user:password_reset_complete"),
                                                                                 template_name = "user/password_reset_confirm.html"), name="password_reset_confirm"),
    path("recover/complete", auth_views.PasswordResetCompleteView.as_view(template_name = "user/password_reset_complete.html"), name="password_reset_complete"),

    path("profile/info/", profileInfoView.as_view(), name="info"),
    path("profile/edit/", profileEditView.as_view(), name="edit"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path('wall/<int:id>/',wallView.as_view(), name="wall"),
]

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
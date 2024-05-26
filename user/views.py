from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
import os
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse, redirect, render,get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.http import HttpResponseRedirect

from home.util import Notification
from home.models import *
from home.views import getSocialAccount
from user.forms import *
from user.tokens import *
import json


class loginView(View):
  def get(self, request):
    if (request.user.is_authenticated):
      return redirect("home:index")
    
    notification_temp = request.session.pop('password_reset_notification', None)
    print(notification_temp["title"] if notification_temp else None)
    print(notification_temp["content"] if notification_temp else None)
    print(notification_temp["status"] if notification_temp else None)
    
    form = LoginForm()
    context = {
      "web": "Login",
      "cssFiles": ["/static/user/login.css",
                   ],
      "form": form,
      "notification":Notification(notification_temp["title"],notification_temp["content"],notification_temp["status"]) if notification_temp else None,
    }
    return render(request, 'user/login.html', context)
  
  def post(self, request):
    form = LoginForm(request, data=request.POST)
    context = {
      "web": "Login",
      "cssFiles": ["/static/user/login.css",
                   ],
      "form": form,
    }
    if form.is_valid():
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(username=username, password=password)
      if user is None:
        print("Wrong login1")
        return redirect("user:login")
      else:
        print("Good login")
        login(request=request, user=user)
        remember_me = request.POST.get('remember_me')
        if not remember_me:
          request.session.set_expiry(0)
        return redirect("home:index")
    else:
      print("Wrongdsdsd login")
      notification = Notification("Login Unsuccessful","Incorrect username or password. Please try again.","error")
      messages.success(request, " ")
      context = {
      "web": "Login",
      "cssFiles": ["/static/user/login.css",
                   ],
      "form": form,
      "notification": notification,
     }
      return render(request, "user/login.html", context)
    

def activate(request, uidb64, token):
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    print(uidb64)
    print(uid)
    user = User.objects.get(username = uid)
  except:
    user = None
  print(user.username)
  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.save()
    messages.success(request, "Create account successfully. You can log in now.")
  else:
    messages.error(request, "Activation link is invalid")
  return redirect("home:index")


class registerView(View):
  def get(self, request):
    usernames = list(User.objects.values_list('username', flat=True))
    emails = list(User.objects.values_list('email', flat=True))
    context = {
      "web": "Register",
      "usernames":usernames,
      "emails":emails,
    }
    return render(request, "user/register.html", context)
  
  def post(self, request):

    email = request.POST.get('Email')

    form_data = {
          'username': request.POST.get('Username'),
          'email': request.POST.get('Email'),
          'password1': request.POST.get('New-password'),
          'password2': request.POST.get('Repeat-new-password'),
          'first_name': request.POST.get('firstname'),
          'last_name': request.POST.get('lastname'),
          'gender':2,
        }

    form = RegisterForm(form_data)
    
    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False
      user.save()
      print(user.username)
      registerView.activateEmail(request, user, form.cleaned_data.get('email'))
      # user.save()

      notification = Notification("Your account is almost ready","Please check your email to activate your account.","success")
      
      usernames = list(User.objects.values_list('username', flat=True))
      emails = list(User.objects.values_list('email', flat=True))
      context = {
        "web": "Register",
        "usernames":usernames,
        "email":email,
        "emails":emails,
        "notification": notification,
      }
      return render(request, "user/register.html", context)
    else:
      print("Form is invalid. Errors:")
      for field, errors in form.errors.items():
          for error in errors:
              print(f"Error in {field}: {error}")

      usernames = list(User.objects.values_list('username', flat=True))
      emails = list(User.objects.values_list('email', flat=True))
      context = {
        "web": "Register",
        "usernames":usernames,
        "emails":emails,
      }
      return render(request, "user/register.html", context)

  def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("user/template_activate_account.html", {
      "user": user.username,
      "domain": get_current_site(request),
      "uid": urlsafe_base64_encode(force_bytes(user.username)),
      "token": account_activation_token.make_token(user),
      "protocol": "https" if request.is_secure() else "http"
    })
    print("Username:", user.username)
    print("Code:", urlsafe_base64_encode(force_bytes(user.pk)))
    print("Current site:", get_current_site(request))
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
      messages.success(request, f'Dear <b>{user.username}</b>, please go to your email <b>{to_email}</b>.')
    else:
      messages.error(request, f'Problem sending email to {to_email}, check if you typed correctly')


class signupRedirect(View):
  def get(self, request):
    messages.error(request, "There are errors when logging in.<br> There might already exist an account with this email.")
    return redirect("user:login")


class logoutView(View):
  def get(self, request):
    logout(request=request)
    return redirect("/")
  

class profileInfoView(LoginRequiredMixin, View):
  login_url = "user:login"
  
  def get(self, request):
    date_join = str(request.user.date_joined.strftime("%d/%m/%Y"))
    date_active = str(request.user.last_login.strftime("%d/%m/%Y"))
    context = {
      "web": "Info",
      "socialAccount": getSocialAccount(request),
      "date_join": date_join,
      "date_active": date_active,
    }
    return render(request, "user/profileInfo.html", context)
  
  def post(self, request):
    pass


class profileEditView(LoginRequiredMixin, View):
  login_url = "user:login"
  def get(self, request):
    form = ProfileEditForm(instance=request.user)
    user = User.objects.get(id=request.user.id)
    birthdate = str(user.birthdate)
    context = {
      "web": "Edit profile",
      "cssFiles": [],
      "form": form,
      "socialAccount": getSocialAccount(request),
      "user":user,
      "birthdate":birthdate,
    }
    return render(request, "user/profileEdit.html", context)
  
  def post(self, request):
    
    
  
    form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      user = User.objects.get(id=request.user.id)
      cleaned_data = form.cleaned_data
      old_avatar = user.avatar.path if user.avatar else None
      print(old_avatar)
      
      if cleaned_data.get('first_name') != '':
        user.first_name = cleaned_data['first_name']
      if cleaned_data.get('last_name') != '':
        user.last_name = cleaned_data['last_name']
      if cleaned_data.get('birthdate'):
        user.birthdate = cleaned_data['birthdate']
      if cleaned_data.get('phoneNum'):
        user.phoneNum = cleaned_data['phoneNum']
      if cleaned_data.get('address'):
        user.address = cleaned_data['address']
      if cleaned_data.get('gender') != '':
        user.gender = cleaned_data['gender']
      if request.FILES.get('avatar'):
        user.avatar = request.FILES['avatar']
        
        
      user.save()
      if request.FILES.get('avatar') and old_avatar:
        print("Removing old avatar")
        if os.path.exists(old_avatar):
          os.remove(old_avatar)
      return redirect("user:info")
    else:
      context = {
        "web": "Edit profile",
        "cssFiles": [],
        "form": form,
        "socialAccount": getSocialAccount(request),
      }
      return render(request, "user/profileEdit.html", context)
    

class changePasswordView(LoginRequiredMixin, View):
  login_url = "user:login"
  
  def get(self, request):
    form = PasswordChangeForm(request.user)
    context = {
      "web": "Change password",
      "cssFiles": [],
      "form": form,
      "socialAccount": getSocialAccount(request),
    }
    return render(request, "user/passwordChange.html", context)
  
  def post(self, request):

    old_password = request.POST.get("old_password")
    new_password1 = request.POST.get("new_password1")
    new_password2 = request.POST.get("new_password2")

    print(old_password, new_password1, new_password2)

    form = PasswordChangeForm(request.user, request.POST)
    context = {
      "web": "Change password",
      "cssFiles": ["/static/user/passwordChange.css",
                  ],
      "form": form,
      "socialAccount": getSocialAccount(request),
    }
    if form.is_valid():
      messages.success(request, 'Your password was successfully updated!')
      notification = Notification("Password Changed Successfully","Your password has been updated successfully. Please use your new password the next time you log in.","success")
      user = form.save()
      update_session_auth_hash(request, user)  # Important!
      context["notification"] = notification
      return render(request, "user/passwordChange.html", context)
    else:
      messages.error(request, 'Please correct the error below.')
      content = form.errors.as_data()

      if 'old_password' in content:
          content = content["old_password"][0].messages[0]
      elif 'new_password2' in content:
          content = content["new_password2"][0].messages[0]
      else:
          content = "An unknown error occurred."

      notification = Notification("A problem has occured",content,"error")
      context["notification"] = notification
      return render(request, "user/passwordChange.html", context)


class wallView(LoginRequiredMixin, View):
  login_url = "user:login"
  def get(self, request, id):
    user = User.objects.get(id=id)
    context = {
      "web": "Wall",
      'wallOwner': user,
      "socialAccount": getSocialAccount(request),
      "form": ThoughtForm(),
      'cssFiles': ["/static/user/wall.css",],
    }
    return render(request, "user/wall.html", context)
  
  def post(self, request, id):
    data = {
      "userID": request.user,
      "thought": request.POST.get("thought"),
      "created_at": timezone.now(),
    }
    form = ThoughtForm(data)
    if form.is_valid():
      form.save()
      messages.success(request, "Your thought has been posted.")
      return redirect("user:wall", id)
    else:
      context = {
        "web": "Wall",
        'wallOwner': User.objects.get(id=id),
        "socialAccount": getSocialAccount(request),
        'cssFiles': ["/static/user/wall.css",],
        "form": form,
      }
      messages.error(request, "Your thought is too long.")
      return render(request, "user/wall.html", context)
  

class recoverAccountView(auth_views.PasswordResetView):
  success_url = reverse_lazy("user:recover")
  email_template_name = "user/recover/recoverEmail.html"
  template_name = "user/recover/recoverForm.html"
  subject_template_name = "user/recover/recoverEmailSubject.txt"
  
  def form_valid(self, form):
    messages.success(self.request, "email sent")
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['notification'] = Notification(
        "Password recover email sent",
        "If your email is associated with an account, you will get a reset link shortly. Please check your inbox.",
        "info"
    )
    context['web'] = "Recover password"
    return context

class recoverDoneView(auth_views.PasswordResetDoneView):
  template_name = "user/recover/recoverDone.html"


class recoverConfirmView(auth_views.PasswordResetConfirmView):
  success_url=reverse_lazy("user:login")
  template_name = "user/recover/recoverConfirm.html"
  
  def form_valid(self, form):
    # Store the notification data in the session
    notification = {
        "title": "Password reset complete",
        "content": "You can now log in with your new password.",
        "status": "success"
    }
    messages.success(self.request, "Password reset complete")
    self.request.session['password_reset_notification'] = notification
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    print("run get context data")
    context = super().get_context_data(**kwargs)
    context['uidb64'] = self.kwargs['uidb64']
    context['token'] = self.kwargs['token']
    context['web'] = "Recover password"
    context['notification'] = Notification(
        "Password reset complete",
        "You can now log in with your new password.",
        "success"
    )
    return context


class recoverCompleteView(auth_views.PasswordResetCompleteView):
  template_name = "user/recover/recoverComplete.html"
  login_url = "user:login"
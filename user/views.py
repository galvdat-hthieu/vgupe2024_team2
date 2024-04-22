from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from home.models import *
from home.views import getSocialAccount
from user.forms import *
from user.tokens import *


class loginView(View):
  def get(self, request):
    if (request.user.is_authenticated):
      return redirect("home:index")
    form = LoginForm()
    context = {
      "web": "Login",
      "cssFiles": ["/static/user/login.css",
                   ],
      "form": form,
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
        return redirect("user:login")
      else:
        login(request=request, user=user)
        remember_me = request.POST.get('remember_me')
        if not remember_me:
          request.session.set_expiry(0)
        return redirect("home:index")
    else:
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
    form = RegisterForm()
    context = {
      "web": "Register",
      "form": form,
    }
    return render(request, "user/register.html", context)
  
  def post(self, request):
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False
      user.save()
      print(user.username)
      registerView.activateEmail(request, user, form.cleaned_data.get('email'))
      # user.save()
      return redirect("/user/login")
    else:
      context = {
        "web": "Register",
        "form": form,
      }
      return render(request, "user/register.html", context)

  def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("user/template_activate_account.html", {
      "user": user.username,
      "domain": get_current_site(),
      "uid": urlsafe_base64_encode(force_bytes(user.username)),
      "token": account_activation_token.make_token(user),
      "protocol": "https" if request.is_secure() else "http"
    })
    print("Username:", user.username)
    print("Code:", urlsafe_base64_encode(force_bytes(user.pk)))
    print("Current site:", get_current_site())
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
      messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b>.')
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
    context = {
      "web": "Info",
      "socialAccount": getSocialAccount(request),
    }
    return render(request, "user/profileInfo.html", context)
  
  def post(self, request):
    pass


class profileEditView(LoginRequiredMixin, View):
  login_url = "user:login"
  def get(self, request):
    form = ProfileEditForm(instance=request.user)
    context = {
      "web": "Edit profile",
      "cssFiles": [],
      "form": form,
      "socialAccount": getSocialAccount(request),
    }
    return render(request, "user/profileEdit.html", context)
  
  def post(self, request):
    form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
      form.save()
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
    form = PasswordChangeForm(request.user, request.POST)
    context = {
      "web": "Change password",
      "cssFiles": ["/static/user/passwordChange.css",
                  ],
      "form": form,
      "socialAccount": getSocialAccount(request),
    }
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)  # Important!
      messages.success(request, 'Your password was successfully updated!')
      return redirect("/")
    else:
      messages.error(request, 'Please correct the error below.')
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
  success_url = reverse_lazy("user:recover_done")
  email_template_name = "user/recover/recoverEmail.html"
  template_name = "user/recover/recoverForm.html"
  subject_template_name = "user/recover/recoverEmailSubject.txt"


class recoverDoneView(auth_views.PasswordResetDoneView):
  template_name = "user/recover/recoverDone.html"


class recoverConfirmView(auth_views.PasswordResetConfirmView):
  success_url=reverse_lazy("user:recover_complete")
  template_name = "user/recover/recoverConfirm.html"


class recoverCompleteView(auth_views.PasswordResetCompleteView):
  template_name = "user/recover/recoverComplete.html"
  login_url = "user:login"
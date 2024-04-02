from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from user.forms import *
from home.models import *
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
        return redirect("home:index")
    else:
      return render(request, "user/login.html", context)
    
def activateEmail(request, user, to_email):
  mail_subject = "Activate your user account."
  message = render_to_string("user/template_activate_account.html", {
    "user": user.username,
    "domain": get_current_site(request).domain,
    "uid": urlsafe_base64_encode(force_bytes(user.username)),
    "token": account_activation_token.make_token(user),
    "protocol": "https" if request.is_secure() else "http"
  })
  print("Username:", user.username)
  print("Code:", urlsafe_base64_encode(force_bytes(user.pk)))
  email = EmailMessage(mail_subject, message, to=[to_email])
  if email.send():
    messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b>.')
  else:
    messages.error(request, f'Problem sending email to {to_email}, check if you typed correctly')

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
      activateEmail(request, user, form.cleaned_data.get('email_address'))
      # user.save()
      return redirect("/user/login")
    else:
      context = {
        "web": "Register",
        "form": form,
      }
      return render(request, "user/register.html", context)


class logoutView(View):
  def get(self, request):
    logout(request=request)
    return redirect("/")
  

class profileInfoView(LoginRequiredMixin, View):
  login_url = "/user/login"
  def get(self, request):
    context = {
      "web": "Info",
      "user": request.user,
    }
    return render(request, "user/profileInfo.html", context)
  
  def post(self, request):
    pass


class profileEditView(LoginRequiredMixin, View):
  def get(self, request):
    form = ProfileEditForm(instance=request.user)
    context = {
      "web": "Edit profile",
      "cssFiles": [],
      "form": form,
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
      }
      return render(request, "user/profileEdit.html", context)
    
class changePasswordView(LoginRequiredMixin, View):
  def get(self, request):
    form = PasswordChangeForm(request.user)
    context = {
      "web": "Change password",
      "cssFiles": [],
      "form": form,
    }
    return render(request, "user/passwordChange.html", context)
  
  def post(self, request):
    form = PasswordChangeForm(request.user, request.POST)
    context = {
      "web": "Change password",
      "cssFiles": ["/static/user/passwordChange.css",
                  ],
      "form": form,
    }
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)  # Important!
      messages.success(request, 'Your password was successfully updated!')
      return redirect("/")
    else:
      messages.error(request, 'Please correct the error below.')
      return render(request, "user/passwordChange.html", context)
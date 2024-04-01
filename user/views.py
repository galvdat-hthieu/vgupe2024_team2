from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from user.forms import *
from home.models import *

class loginView(View):
  def get(self, request):
    if (request.user.username):
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
        return redirect("user:info")
    else:
      return render(request, "user/login.html", context)
    

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
    address = request.POST.get("email_address")
    print(address)
    if form.is_valid():
      form.save()
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
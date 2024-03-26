from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from user.forms import RegisterForm, LoginForm
from home.models import *

class loginView(View):
  def get(self, request):
    form = LoginForm()
    context = {
      "web": "Login",
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
        return redirect("/user/login")
      else:
        login(request=request, user=user)
        return render(request, "user/info.html", context)
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

class infoView(LoginRequiredMixin, View):
  login_url = "/user/login"
  def get(self, request):
    context = {"user": request.user}
    return render(request, "user/info.html", context)
  
  def post(self, request):
    pass

class logoutView(View):
  def get(self, request):
    logout(request=request)
    return redirect("/")

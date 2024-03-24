from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from user.forms import RegisterForm

class loginView(View):
  def get(self, request):
    return render(request, 'user/login.html')
  
  def post(self, request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
      return HttpResponse("User khong ton tai")
    else:
      login(request=request, user=user)
      return render(request, "user/info.html")
    

class registerView(View):
  def get(self, request):
    form = RegisterForm()
    context = {
      "web": "Register",
      "form": form
    }
    return render(request, "user/register.html", context)
  
  def post(self, request):
    form = RegisterForm(request.POST)

    if form.is_valid():
      form.save()
      return redirect("/user/login")


class infoView(LoginRequiredMixin, View):
  login_url = "/user/login"
  def get(self, request):
    context = {"user": request.user}
    return render(request, "user/info.html", context)
  
  def post(self, request):
    pass
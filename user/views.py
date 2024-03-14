from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


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
    

class infoView(LoginRequiredMixin, View):
  login_url = "/user/login"
  def get(self, request):
    context = {"user": request.user}
    return render(request, "user/info.html", context)
  
  def post(self, request):
    pass
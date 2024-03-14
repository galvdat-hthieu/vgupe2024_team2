from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
def index(request):
  return render(request, 'index.html')

class loginView(View):
  def get(request):
    return render('home/login.html', request)
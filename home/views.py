from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

# Create your views here.
def index(request):
  return render(request, 'home/index.html')

class galleryView(LoginRequiredMixin, View):
  login_url = "/user/login"

  def get(self, request):
    books = Book.objects.all()
    context = {
      "user": request.user,
      "books": books,
    }
    return render(request, "home/gallery.html", context)
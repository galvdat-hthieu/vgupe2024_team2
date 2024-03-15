from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.db.models import Q


# Create your views here.
def index(request):
  return render(request, 'home/index.html')

def search(request):

  books = Book.objects.all()
  cateList = ['liteCate','socieCate','naturCate','techCate','poliCate','romanCate','enterCate','otherCate']

  

  if request.GET.get("book_search"):
    keyword = request.GET.get("book_search")
    books = Book.objects.filter(title__contains = keyword)
    

  if request.GET.getlist("category"):
    selected_categories = request.GET.getlist('category')
    filter_condition = Q()
    for category in selected_categories:
      filter_condition &= Q(**{category: True})
    books = books.filter(filter_condition)
      

  context = {
    'books':books
  }

  return render(request, 'home/gallery.html',context)

class galleryView(LoginRequiredMixin, View):
  login_url = "/user/login"

  def get(self, request):
    books = Book.objects.all()
    context = {
      "user": request.user,
      "books": books,
    }
    return render(request, "home/gallery.html", context)
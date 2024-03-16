from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.db.models import Q


# Create your views here.
class indexView(View):
  def get(self, request):
    return render(request, 'home/index.html')


class searchView(View):
  def get(self, request):

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

    return render(request, 'home/search.html',context)


class galleryView(View):
  def get(self, request):
    books = Book.objects.all()
    context = {
      "web": "Gallery",
      "user": request.user,
      "books": books,
    }
    return render(request, "home/gallery.html", context)
  

class registerView(View):
  def get(self, request):
    context = {
      "web": "Register"
    }
    return render(request, "home/register.html", context)
  
  def post(self, request):
    pass
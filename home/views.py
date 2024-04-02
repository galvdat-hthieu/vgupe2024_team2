from autocorrect import Speller
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views import View
from django.utils import timezone
from word_forms.word_forms import get_word_forms
from .forms import *
from .models import *
import os

# Create your views here.
class indexView(View):
  def get(self, request):
    return render(request, 'home/index.html')


class searchView(View):
  def get(self, request):
    booksByKeyword = Book.objects.none()

    if request.GET.get("book_search"):
      keyword = request.GET.get("book_search").strip()
      spell = Speller(lang='en')
      spell_corrected_keyword = spell(keyword)
      wordForms = get_word_forms(spell_corrected_keyword)
      wordFormsList = [keyword,spell_corrected_keyword]
      if len(wordForms['n']) != 0:
          wordFormsList.extend(wordForms['n'])
      if len(wordForms['a']) != 0:
          wordFormsList.extend(wordForms['a'])
      if len(wordForms['v']) != 0:
          wordFormsList.extend(wordForms['v'])
      if len(wordForms['r']) != 0:
          wordFormsList.extend(wordForms['r'])
      
      for keyword in wordFormsList:
        booksByTitle = Book.objects.filter(title__icontains=keyword)
        booksByAuthor = Book.objects.filter(author__icontains=keyword)
        booksByKeyword |= booksByTitle | booksByAuthor

    else:
      booksByKeyword = Book.objects.all()
        
      
    booksByCategories = Book.objects.none()  

    if request.GET.getlist("category"):
      selected_categories = request.GET.getlist('category')
      filter_condition = Q()
      for category in selected_categories:
        filter_condition &= Q(**{category: True})
      booksByCategories = Book.objects.filter(filter_condition)
    else:
      booksByCategories = Book.objects.all()  
    
    books = booksByKeyword & booksByCategories
    context = {
      "books": books,
      "cssFiles": ["/static/home/gallery.css",
                   "/static/home/search.css"],
    }

    return render(request, 'home/search.html',context)


class galleryView(View):
  def get(self, request):
    books = Book.objects.all()
    context = {
      "web": "Gallery",
      "cssFiles": ["/static/home/gallery.css",
                  ],
      "user": request.user,
      "books": books,
    }
    return render(request, "home/gallery.html", context)


class bookView(View):
  def get(self, request, id):
    book = Book.objects.get(id=id)
    form = ReviewForm(initial={"bookID": Book.objects.get(id=id),"userID": request.user,})
    context = {
      'book': book,
      "form": form,
      "time": timezone.now()
    }



    return render(request, "home/book.html", context)
  
  def post(self, request, id):
    form = ReviewForm(request.POST)
  
    if form.is_valid():
      new_review = form.save(commit=False)
      new_review.user = request.user.username
      new_review.save()
      return HttpResponseRedirect('#')
    
    return render(request, "home/book.html", {'form': form})
      
          
class vendorView(View):
  def get(self, request, username):
  
    vendor = User.objects.get(username=username)
    books = Book.objects.filter(ownerID=vendor.id)
    totalAmount = books.count()
    print(totalAmount)
    context = {
    'vendor': vendor,
    'books':books,
    'totalAmount':totalAmount
    }

    return render(request, "mod/modVendor.html",context)
  def post(self, request, username):

    return render(request, "mod/modVendor.html")

def readPDF(request, id):
  book = Book.objects.get(id=id)


  context = {
    'book':book,
    }

  return render(request, "home/pdf.html", context)
  


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
    context = {
      "web":"Home"
    }
    return render(request, 'home/index.html',context)


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
      "web":"Search",
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
      "web": book.title,
      "cssFiles": ["/static/home/book.css",
                   ],
      "time": timezone.now(),
      'book': book,
      "form": form,
    }



    return render(request, "home/book.html", context)
  
  def post(self, request, id):
    form = ReviewForm(request.POST)
    book = Book.objects.get(id=id)
    if form.is_valid():
      form.save()
      messages.success(request, "Your rating and review has been saved.")
      return redirect("home:book", id)
    else:
      context = {
      "web": book.title,
      "cssFiles": ["/static/home/book.css",
                   ],
      "time": timezone.now(),
      "book": book,
      "form": form,
      }
      messages.error(request, "Your rating and review need to follow the format.")
      return render(request, "home/book.html", context)
      
class bookPDFView(View):
  def get(self, request, id):
    book = Book.objects.get(id=id)
    context = {
      "web": book.title,
      "cssFiles": [],
      "time": timezone.now(),
      'book': book,
    }
    return render(request, "home/pdfDisplay.html", context)
          
class vendorView(View):
  def get(self, request, username):
  
    vendor = User.objects.get(username=username)
    books = Book.objects.filter(ownerID=vendor.id)
    totalAmount = books.count()
    print(totalAmount)
    context = {
    "web":vendor.first_name,
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
  


from autocorrect import Speller
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
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
    copies = Copy.objects.filter(bookID=book)
    mod_counts = copies.values('userID').annotate(count=Count('id'))
    mod_counts_dict = {item['userID']: item['count'] for item in mod_counts}
    mod_ids = mod_counts_dict.keys()
    mods = User.objects.filter(pk__in=mod_ids)
    mods_objects_dict = {mod: mod_counts_dict[mod.id] for mod in mods}

    form = ReviewForm(initial={"bookID": Book.objects.get(id=id),"userID": request.user,})
    context = {
      "web": book.title,
      "cssFiles": ["/static/home/book.css",
                   ],
      "time": timezone.now(),
      'book': book,
      "form": form,
      "mods_objects_dict":mods_objects_dict,
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
    copies = Copy.objects.filter(userID_id=vendor.id,status=1)
    books = Book.objects.filter(id__in=copies.values('bookID_id'))

    totalBooks = books.count()
    totalCopies = copies.count()

    context = {
    "web":vendor.first_name,
    'vendor': vendor,
    'books': books,
    'totalBooks': totalBooks,
    'totalCopies': totalCopies,
    }

    return render(request, "mod/modVendor.html",context)
  def post(self, request, username):

    return render(request, "mod/modVendor.html")


  

class borrowView(View):
  def get(self, request):
    return render(request, "home/borrowance.html")

  def post(self, request):
    if request.method == 'POST':
        userID = request.POST.get("userID")
        if userID == "None":
          return redirect("user:login")
        else:
          modName = request.POST.get("source")  
          mod = User.objects.get(first_name=modName)
          bookID = request.POST.get("bookID")
          book = Book.objects.get(id=bookID)
          copy = Copy.objects.filter(userID_id=mod.id, bookID_id=book.id).first()

          context = {
              'mod':mod,
              'book':book,
              'copy':copy,
          }
          return render(request, "home/borrowance.html", context)
      
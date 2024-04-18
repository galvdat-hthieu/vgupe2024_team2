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
from allauth.socialaccount.models import SocialAccount
import os

# Create your views here.
def getSocialAccount(request):
  if (request.user.is_authenticated):
    try:
      socialAccount = SocialAccount.objects.get(user = request.user)
    except SocialAccount.DoesNotExist:
      socialAccount = None
  else:
    socialAccount = None
  return socialAccount


class indexView(View):
  def get(self, request):
    context = {
      "web":"Home",
      "cssFiles": [],
      "socialAccount": getSocialAccount(request),
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
      "cssFiles": ["/static/home/panel.css",
                   "/static/home/search.css"],
      "socialAccount": getSocialAccount(request),
    }

    return render(request, 'home/search.html',context)


class galleryView(View):
  def get(self, request):
    books = Book.objects.all()
    context = {
      "web": "Gallery",
      "cssFiles": ["/static/home/panel.css",
                  ],
      "user": request.user,
      "socialAccount": getSocialAccount(request),
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
      "socialAccount": getSocialAccount(request),
      "mods_objects_dict":mods_objects_dict,
    }
    return render(request, "home/book.html", context)
  
  def post(self, request, id):
    data = {
      "bookID": Book.objects.get(id=id),
      "userID": request.user,
      "rating": request.POST.get("rating"),
      "review": request.POST.get("review"),
      "created_at": timezone.now(),
    }
    form = ReviewForm(data)
    book = Book.objects.get(id=id)
    if form.is_valid():
      print("User:",form.data["userID"])
      print("Book",form.data["bookID"])
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
      "socialAccount": getSocialAccount(request),
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
      "socialAccount": getSocialAccount(request),
    }
    return render(request, "home/pdfDisplay.html", context)


class shelfView(View):
  template = "home/shelf.html"

  def get(self, request, id):
    vendor = User.objects.get(id=id)
    copies_1 = Copy.objects.filter(userID_id=vendor.id)
    books = Book.objects.filter(id__in=copies_1.values('bookID_id'))
    copies_2 = []
    for i in range(0, len(books)):
      copies_2.append(Copy.objects.filter(userID_id=vendor.id, bookID_id = books[i].id))
    context = {
      "web":vendor.first_name,
      "cssFiles": ["/static/home/shelfItem.css"],
      'vendor': vendor,
      'books': books,
      'copies': copies_1,
      'copies_2': copies_2,
      "socialAccount": getSocialAccount(request),
    }

    return render(request, self.template, context)
  def post(self, request, username):

    return render(request, self.template)


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
      
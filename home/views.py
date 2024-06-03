from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views import View
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from home.forms import *
from home.models import *
from home.functions import *
import os, random, time
from home.util import Notification

# Create your views here.



class indexView(View):
  def get(self, request):
    context = {
      "web":"Home",
      "cssFiles": [],
      "socialAccount": getSocialAccount(request),
      "books": {
        "random": Book.objects.get(id = random.randint(1, len(Book.objects.all()))),
        "literature": random.sample(list(Book.objects.filter(liteCate = 1)), 6),
        "trending": random.sample(list(Book.objects.all()), 6),
        "favorite": random.sample(list(Book.objects.all()), 6),
      }
    }
    return render(request, 'home/index.html',context)

class faqView(View):
  def get(self, request):
    context = {
      "web":"FAQ",
      "cssFiles": [],
      "socialAccount": getSocialAccount(request),
    }
    return render(request, 'home/faq.html',context)

class contactView(View):
  def get(self, request):
    context = {
      "web":"Contact",
      "cssFiles": [],
      "socialAccount": getSocialAccount(request),
    }
    return render(request, 'home/contact.html',context)


class galleryView(View):
  def get(self, request):
    books = search(request)
    print(len(books))
    
    page = request.GET.get('page', 1)
    paginator = Paginator(books, 10)
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
        
    min = paginator.num_pages - 4
    max = paginator.num_pages
    
    context = {
      "web":"Search",
      "books": books,
      "cssFiles": ["/static/home/panel.css",
                   "/static/home/search.css"],
      "socialAccount": getSocialAccount(request),
      "min":min,
      "max":max
    }
    return render(request, 'home/gallery.html',context)


class bookView(View):
  def get(self, request, id):
    
    notification_temp = request.session.pop('review_submit', None)
    
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
      "notification":Notification(notification_temp["title"],notification_temp["content"],notification_temp["status"]) if notification_temp else None,
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

      form.save()
      notification = {
        "title": "Review sent successfully.",
        "content": "Your review has been sent successfully. Thank you for your feedback.",
        "status": "success"
      }  
      messages.success(request, "Profile info updated successfully.")
      request.session['review_submit'] = notification
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
    
def handling_404(request, exception):
  context = {
    "web":"Page not found",
    "socialAccount": getSocialAccount(request),
  }
  return render(request, '404.html',context)
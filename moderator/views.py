from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib import messages
from .forms import BookForm, CopyForm
from home.models import *

# Create your views here.
class modView(View):
  def get(self, request):
    return HttpResponse('Moderator page')
  
  def post(self, request):
    pass


class addBookView(View):
  def get(self, request):
    if (request.user.is_authenticated and request.user.role >= 1):
      form = BookForm()
      context = {
        "web": "Add Copy",
        "cssFiles": [],
        "form": form,
      }
      return render(request, 'mod/addBook.html', context)
    else:
      messages.error(request, "You don't have the right to add book.")
      return redirect("home:index")

  def post(self, request):
    form = BookForm(request.POST, request.FILES)
    context = {
      "web": "Add Copy",
      "cssFiles": [],
      "form": form,
    }
    if form.is_valid():
      form.save()
      messages.success(request,f"Book is added successfylly.")
      return redirect("home:gallery")
    else:
      return render(request, 'mod/addBook.html', context)

class addCopyView(View):
  def get(self, request, id):
    book = Book.objects.get(id = id)
    form = CopyForm(initial={"bookID": book,
                             "userID": request.user,})
    if (request.user.is_authenticated and request.user.role >= 1):
      context = {
          "web": "Add Copy",
          "cssFiles": [],
          "book": book,
          "form": form,
      }
      return render(request, 'mod/addCopy.html', context)
    else:
      messages.error(request, "You don't have the right to add copy.")
      return redirect("home:index")
  
  def post(self, request, id):
    form = CopyForm(request.POST)
    book = Book.objects.get(id = id)
    if (request.user.is_authenticated and request.user.role >= 1):
      if form.is_valid():
        form.save()
        messages.success(request, "Your copy has been added successfully.")
        return redirect("home:book", id)
      else:
        context = {
            "web": "Add Copy",
            "cssFiles": [],
            "book": book,
            "form": form,
        }
        messages.error(request, "There is a problem with adding your copy.")
        return render(request, 'mod/addCopy.html', context)
    else:
      messages.error(request, "You don't have the right to add copy.")
      return redirect("home:index")
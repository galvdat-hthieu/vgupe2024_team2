from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib import messages
from .forms import BookForm, CopyForm
from home.models import *
from datetime import date
import csv
import sqlite3
from django.db import connections

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
        "jsFiles": ["/static/mod/addBook.js",
                  ],
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
      "jsFiles": ["/static/mod/addBook.js",
                  ],
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
    if not (request.user.is_authenticated and request.user.role >= 1):
      messages.error(request, "You don't have the right to add copy.")
      return redirect("home:index")
    book = Book.objects.get(id = id)
    form = CopyForm(initial={"bookID": book,
                             "userID": request.user,
                             "regDate": date.today()})
    context = {
      "web": "Add Copy",
      "cssFiles": [],
      "book": book,
      "form": form,
    }
    return render(request, 'mod/addCopy.html', context)
  
  def post(self, request, id):
    form = CopyForm(request.POST)
    book = Book.objects.get(id = id)
    if not (request.user.is_authenticated and request.user.role >= 1):
      messages.error(request, "You don't have the right to add copy.")
      return redirect("home:index")
    if form.is_valid():
      form.bookID = book
      form.userID = request.user
      form.regDate = date.today()
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
    

class editBookView(View):
  def get(self, request, id):
    if not(request.user.is_authenticated and request.user.role >= 1):
      messages.error(request, "You don't have the right to edit book.")
      return redirect("home:index")
    book = Book.objects.get(id = id)
    form = BookForm(instance=book)
    context = {
      "web": "Edit Book",
      "cssFiles": [],
      "book": book,
      "form": form,
    }
    return render(request, "mod/editBook.html", context)

  def post(self, request, id):
    if not(request.user.is_authenticated and request.user.role >= 1):
      messages.error(request, "You don't have the right to edit book.")
      return redirect("home:index")
    book = Book.objects.get(id = id)
    form = BookForm(request.POST, request.FILES, instance=book)
    if form.is_valid():
      form.save()
      messages.success(request, "The book has been edited succesfully.")
      return redirect("home:book", id)
    else:
      context = {
        "web": "Edit Book",
        "cssFiles": [],
        "book": book,
        "form": form,
      }
      return render(request, "mod/editBook.html", context)
    

class importDataView(View):
  def get(self, request):
    # Establish a connection to the SQLite3 database
    database_path = 'db.sqlite3'
    connection = sqlite3.connect(database_path)

    # Get the cursor
    cursor = connection.cursor()

    # Open the CSV file and read its contents
    csv_file_path = 'books4.csv'
    with open(csv_file_path, 'r', encoding='cp437') as file:
      reader = csv.reader(file, delimiter=';')
      next(reader)  # Skip the header row

      count = 0
      # Iterate over each row in the CSV file
      for row in reader:
        count = count + 1
        print(count)
        print(row)
        row = row[0].replace('"','')
        row = row.split(";")
        new_row = []
        for i in range(0, len(row)):
          if i not in [5, 6]:
            new_row.append(row[i])
        print(new_row[0:6])
        # Insert the row data into the books table
        try: 
          cursor.execute('''
              INSERT INTO home_book (codeISBN, title, author, publication, publisher, coverImage, type, liteCate, socieCate, naturCate, techCate, poliCate, romanCate, enterCate, otherCate, language, status)
              VALUES (?, ?, ?, ?, ?, ?, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'English', 1)
          ''', new_row[0:6])
        except:
          print("An exception occured")


    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    # Optional: Refresh Django's database connections
    connections.close_all()
    return HttpResponse("Finished")
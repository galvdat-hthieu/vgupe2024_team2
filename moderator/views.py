from django.shortcuts import render
from django.http import HttpResponse
from .forms import BookForm


# Create your views here.
def mod(request):
    return HttpResponse('Moderator page')

def add_book(request):
    a = BookForm()
    return render(request, 'book/add_book.html', {'f': a})

def save(request):
    if request.method == 'POST':
        a = BookForm(request.POST, request.FILES)
        if a.is_valid():
            a.save()
            return HttpResponse('Book added successfully')
        else:
            return HttpResponse('Invalid data')
    else:
        return HttpResponse('Invalid method')
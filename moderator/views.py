from django.shortcuts import render, HttpResponse
from django.views import View
from .forms import BookForm, CopyForm


# Create your views here.
class modView(View):
    def get(self, request):
        return HttpResponse('Moderator page')


class addBookView(View):
    def get(self, request):
        a = BookForm()
        return render(request, 'mod/addBook.html', {'f': a})

class saveBookView(View):
    def post(self, request):
        if request.method == 'POST':
            a = BookForm(request.POST, request.FILES)
            if a.is_valid():
                saved_book = a.save()
                book_id = saved_book.id
                return HttpResponse(f'Book added successfully with ID: {book_id}')
            else:
                return HttpResponse('Invalid data')
        else:
            return HttpResponse('Invalid method')

class addCopyView(View):
    def get(self, request):
        b = CopyForm()
        return render(request, 'mod/addCopy.html', {'f': b})

class saveCopyView(View):
    def post(self, request):
        if request.method == 'POST':
            b = CopyForm(request.POST)
            if b.is_valid():
                saved_copy = b.save()
                copy_id = saved_copy.id
                return HttpResponse(f'Copy added successfully with ID: {copy_id}')
            else:
                return HttpResponse('Invalid data')
        else:
            return HttpResponse('Invalid method')
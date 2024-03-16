from django.shortcuts import render, HttpResponse
from django.views import View
from .forms import BookForm


# Create your views here.
class modView(View):
    def get(self, request):
        return HttpResponse('Moderator page')


class addBookView(View):
    def get(self, request):
        a = BookForm()
        return render(request, 'mod/addBook.html', {'f': a})

    def post(self, request):
        if request.method == 'POST':
            a = BookForm(request.POST, request.FILES)
            if a.is_valid():
                a.save()
                return HttpResponse('Book added successfully')
            else:
                return HttpResponse('Invalid data')
        else:
            return HttpResponse('Invalid method')
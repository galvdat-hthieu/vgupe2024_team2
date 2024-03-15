from django import forms
from .models import Book

# create the form here.
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
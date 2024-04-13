from django import forms
from home.models import Book, Copy

# create the form here.
class BookForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = '__all__'

class CopyForm(forms.ModelForm):
  class Meta:
    model = Copy
    fields = '__all__'
    widgets = {
      "regDate": forms.DateInput(attrs={"type": "date"}),
      "bookID": forms.HiddenInput(),
      "userID": forms.HiddenInput(),
    }

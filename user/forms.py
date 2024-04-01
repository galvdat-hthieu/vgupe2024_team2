from home.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
  class Meta:
    model = User
    fields = "__all__"


class RegisterForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email_address", "password1", "password2",
              "first_name", "last_name", "birthdate", "gender",
              "address", "phoneNum"]
    # fields = "__all__"

  def clean(self):
    email = self.cleaned_data.get('email_address')
    if User.objects.filter(email_address=email).exists():
        raise ValidationError("Email exists")
    return self.cleaned_data

class ProfileEditForm(forms.ModelForm):

  class Meta:
    model = User
    fields = ["avatar", "first_name", "last_name", "birthdate", "gender",
              "address", "phoneNum"]
    

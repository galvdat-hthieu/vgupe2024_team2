from home.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
  class Meta:
    model = User
    fields = "__all__"


class RegisterForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2",
              "first_name", "last_name", "birthdate", "gender",
              "address", "phoneNum"]
    # fields = "__all__"
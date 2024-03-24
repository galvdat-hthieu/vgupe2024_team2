from home.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]
    # fields = "__all__"
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import *
from home.functions import *

class ControlView(LoginRequiredMixin, View):
  login_url = "home:login"

  def get(self, request):
    if not (request.user.role == 2):
      messages.error(request, "You are not allowed to access")
    persons = User.objects.all()
    context = {
      "web": "Control",
      "cssFiles": [],
      "jsFiles": [],
      "persons": persons,
    }
    return render(request, "control/control.html", context)
  
  def post(self, request):
    pass

class ModApplyView(LoginRequiredMixin, View):
  login_url = "home:login"
  template_url = "control/review/modReview.html"

  def get(self, request):
    context = {
      "web": "Mod Review",
      "applications": ModApplication.objects.all(),
      "socialAccount": getSocialAccount(request),
    }
    return render(request, self.template_url, context)
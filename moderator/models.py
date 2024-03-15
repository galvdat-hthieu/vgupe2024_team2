from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, null=False, default="UNTITLED")
    author = models.CharField(max_length=200, null=False, default="UNKNOWN")
    language = models.CharField(max_length=200, null=True, blank=True)
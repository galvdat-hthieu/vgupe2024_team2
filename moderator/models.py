from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, null=False, default="UNTITLED")
    author = models.CharField(max_length=200, null=False, default="UNKNOWN")
    typeChoices = (
    (0, "Article"),
    (1, "Book"),
    (2, "Magazine"),
    (3, "Video/Audio"),
    (4, "Comic"),
    (5, "Other")
    )
    type = models.IntegerField(choices=typeChoices, null=False, default = 1)
    liteCate = models.BooleanField(default=False, blank=True)
    socieCate = models.BooleanField(default=False, blank=True)
    naturCate = models.BooleanField(default=False, blank=True)
    techCate = models.BooleanField(default=False, blank=True)
    poliCate = models.BooleanField(default=False, blank=True)
    romanCate = models.BooleanField(default=False, blank=True)
    enterCate = models.BooleanField(default=False, blank=True)
    otherCate = models.BooleanField(default=False, blank=True)
    language = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1500, null=True, blank=True)
    coverImage = models.ImageField(upload_to="data/book/coverImage", null=True, blank=True)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    publication = models.CharField(max_length=50, null=True, blank=True)
    codeISBN = models.CharField(max_length=50, null=True, blank=True)
    
    statusChoices = (
    (0, "Pending"),
    (1, "Accepted"),
    (2, "Rejected")
    )
    status = models.IntegerField(choices=statusChoices, null=False,default=0)

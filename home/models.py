from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=200, null=False, default="UNTITLED")
  author = models.CharField(max_length=200, null=False, default="UNKNOWN")
  typeChoices = (
    (0, "article"),
    (1, "book"),
    (2, "magazine"),
    (3, "video/audio"),
    (4, "comic"),
    (5, "other")
  )
  type = models.IntegerField(choices=typeChoices, null=False)
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
  pdfFile = models.FileField(upload_to="data/book/pdf",null=True,blank=True)
  publisher = models.CharField(max_length=200, null=True, blank=True)
  publication = models.CharField(max_length=50, null=True, blank=True)
  codeISBN = models.CharField(max_length=50, null=True, blank=True)
  statusChoices = (
    (0, "pending"),
    (1, "accepted"),
    (2, "rejected")
  )
  status = models.IntegerField(choices=statusChoices, default=0)
  id = models.AutoField(primary_key=True)

  def __str__(self) :
    return str(self.id) + ". " + self.title


class User(AbstractUser):
  avatar = models.ImageField(upload_to="data/user/avatar/", null=True, blank=True)
  birthdate = models.DateField(null=True, blank=True)
  genderChoices = (
    (0, "male"),
    (1, "female"),
    (2, "other")
  )
  gender = models.IntegerField(choices=genderChoices, null=False, default=2)
  address = models.CharField(max_length=200, null=True, blank=True)
  phoneNum = models.CharField(max_length=50, null=True, blank=True)
  roleChoices = (
    (0, "user"),
    (1, "moderator"),
    (2, "admin"),
    (3, "banned")
  )
  role = models.IntegerField(choices=roleChoices, default=0)


class Copy(models.Model):
  bookID = models.ForeignKey(Book, null=False, on_delete=models.CASCADE)
  userID = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
  statusChoices = (
    (0, "hidden"),
    (1, "available"),
    (2, "borrowed"),
    (3, "unavailable")
  )
  status = models.IntegerField(choices=statusChoices, default=0)
  note = models.CharField(max_length=200, null=True, blank=True)
  regDate = models.DateTimeField(null=False)


class Borrowance(models.Model):
  copyID = models.ForeignKey(Copy, on_delete=models.CASCADE)
  userID = models.ForeignKey(User, on_delete=models.CASCADE)
  borrowDate = models.DateTimeField(null=False)
  expiredDate = models.DateTimeField(null=False)
  statusChoices = (
    (0, "request"),
    (1, "double-check"),
    (2, "borrowing"),
    (3, "returned"),
    (4, "overdue"),
    (5, "lost")
  )
  status = models.IntegerField(choices=statusChoices, default=0, null=False)
  deposit = models.FloatField(default=0, null=True, blank=True)


class Review(models.Model):
  bookID = models.ForeignKey(Book, on_delete=models.CASCADE)
  userID = models.ForeignKey(User, on_delete=models.CASCADE)

  def validateRating(value):
    if (value > 5 or value < 1):
      raise ValidationError(
        _('%(value)s is not valid'),
        params={'value': value},
      )
    
  rating = models.IntegerField(validators=[validateRating], null=True, blank=True)
  review = models.TextField(max_length=1500, null=True, blank=True)
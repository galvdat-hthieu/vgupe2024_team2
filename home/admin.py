from django.contrib import admin
from .models import Book, User, Review, Borrowance, Copy

# Register your models here.

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Borrowance)
admin.site.register(Copy)
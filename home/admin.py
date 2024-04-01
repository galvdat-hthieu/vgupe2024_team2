from django.contrib import admin
from .models import Book, User, Review, Borrowance, Copy

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', "publisher", "language", "codeISBN")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", 'username', "email_address")

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", 'bookID', 'userID', 'rating', 'created_at')

class BorrowanceAdmin(admin.ModelAdmin):
    list_display = ('id', "copyID", "userID", "status")

class CopyAdmin(admin.ModelAdmin):
    list_display = ('id', "bookID", "userID")

admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Borrowance, BorrowanceAdmin)
admin.site.register(Copy, CopyAdmin)
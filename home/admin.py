from django.contrib import admin
from .models import Book, User, Review, Borrowance, Copy

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('bookID', 'userID', 'rating', 'created_at')

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Borrowance)
admin.site.register(Copy)
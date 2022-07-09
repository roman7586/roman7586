
from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "categoryType", "dateCreation", "getpostCategory", "title", "text", "rating")

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
#admin.site.unregister(Post) таким образом можно удалить модель в админскойДжанго
admin.site.register(PostCategory)
admin.site.register(Comment)



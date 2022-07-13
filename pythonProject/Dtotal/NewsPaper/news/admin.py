
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

from .models import Author, Category, Post, PostCategory, Comment
from modeltranslation.translator import register, \
    TranslationOptions  # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "categoryType", "dateCreation", "getpostCategory", "title", "rating") # оставляем необходимые данные
    list_filter = ("author", "categoryType", "dateCreation") # добавляем примитивные фильтры в нашу админку

# регистрируем наши модели для перевода

class CategoryAdmin(TranslationAdmin):
    model = Category

class PostlAdmin(TranslationAdmin):
    model = Post

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
#admin.site.unregister(Post) таким образом можно удалить модель в админскойДжанго
admin.site.register(PostCategory)
admin.site.register(Comment)

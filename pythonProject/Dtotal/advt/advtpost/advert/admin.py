from django.contrib import admin

# Register your models here.
from .models import Post, Otvet

admin.site.register(Post)
admin.site.register(Otvet)
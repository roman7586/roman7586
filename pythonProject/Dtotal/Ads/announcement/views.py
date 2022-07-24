from django.shortcuts import render

# Create your views here.
from .models import Post


def home_page (request):
    data = Post.objects.all()
    return render(request, 'homepage.html', {'data': data})
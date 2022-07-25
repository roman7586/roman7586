from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Post


def home_page(request):
    data = Post.objects.all()
    return render(request, 'home_page.html', {'data': data})

class PostsList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'home_page.html'
    context_object_name = 'posts'
    paginate_by = 10

    #def get_queryset(self):
    #    # Получаем обычный запрос
    #    queryset = super().get_queryset()
    #    # Используем наш класс фильтрации.
    #    # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
    #    # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
    #    self.filterset = PostFilter(self.request.GET, queryset)
    #    # Возвращаем из функции отфильтрованный список товаров
    #    return self.filterset.qs
    #
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    # Добавляем в контекст объект фильтрации.
    #    context['filterset'] = self.filterset
    #    return context

class PostDetail(DetailView):
    model = Post
    template_name = 'more.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'
#абзац по кэшу
    queryset = Post.objects.all()

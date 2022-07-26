from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView

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
    #queryset = Post.objects.all()

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'account/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

#Включение авторства по кнопке
@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

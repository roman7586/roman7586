from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView

from .forms import PostForm
from .models import Post, Otvet


def home_page(request):
    data = Post.objects.all()
    return render(request, 'posts.html', {'data': data})

class PostsList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'more.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView): #PermissionRequiredMixin
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    permission_required = ('Ads.add_post',)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('')





class MyResponses(ListView):
    model = Post
    template_name = 'otvety.html'
    context_object_name = 'board'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = Otvet.objects.filter(response_to__user=self.request.user)
        return context



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/index.html'

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

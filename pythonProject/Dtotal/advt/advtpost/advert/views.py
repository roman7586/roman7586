from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .filters import PostFilter
from .forms import PostForm, NewsForm
from .models import Post, Otvet


class PostsList(ListView): #Общий список обьявлений
    model = Post
    ordering = 'dateCreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class MyPosts(ListView): #Список только своих созданных обьявлений
    model = Post
    ordering = 'dateCreation'
    template_name = 'myposts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class PostDetail(DetailView): #Полная информация о выбранном обьявлении
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(LoginRequiredMixin, CreateView): #Создание обьявления
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('advert.add_post',)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdate(LoginRequiredMixin, UpdateView): #Изменение обьявления
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('advert.change_post', )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostDelete(LoginRequiredMixin, DeleteView): #Удаление обьявления
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('')


class OtckliksMyPost(LoginRequiredMixin, ListView): #Список откликов
    model = Otvet
    ordering = 'dateCreation'
    template_name = 'otklickto.html'
    context_object_name = 'Otvets'
    paginate_by = 10

    def get_queryset(self):
        queryset = Otvet.objects.filter(Otvet_to__user=self.request.user)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset']=self.filterset
        return context


class OtclickToPost(LoginRequiredMixin, CreateView): #Создание отклика
    model = Otvet
    fields = ['text',]
    template_name = 'otclick.html'
    success_url = "posts/{}"
    context_object_name = 'otclick'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.Otvet_user = self.request.user
        self.object.Otvet_to_id = self.kwargs.get('pk')
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')})

class DeleteOtklick(LoginRequiredMixin, DeleteView): # Удаление отклика
    model = Otvet
    template_name = 'otklick_delete.html'
    success_url = '/posts/otklicks/'

@login_required # Утверждение отклика
def confirm(request, id):
    otvet = Otvet.objects.get(pk=id)
    otvet.confirm = True
    otvet.save()

    post_author = otvet.Otvet_to.user.username
    post_id = otvet.Otvet_to.id
    otvet_user = otvet.Otvet_user.username
    email = otvet.Otvet_user.email

    send_mail(
        subject=post_author,
        message=f"Добрый день, {otvet_user}\n"
                f"Ваш отклик на обьявление №{post_id} от автора {post_author} был просмотрен и утверждён!",
        from_email='',
        recipient_list=[email])
    return HttpResponseRedirect(f'/posts/otklicks/')


def newssend(request): # Рассылка сообщения|новостей всем пользователям
    form = NewsForm(request.POST)
    if form.is_valid():
        form.save()
        subject = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        mail_list = [mail for mail in User.objects.all().values_list('email', flat=True)[1:]]
        send_mail(
            f'{subject}',
            f'{text}',
            mail_list
        )
        return redirect('/')
    return render(request, 'allsend.html', {'form': form})
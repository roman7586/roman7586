from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .filters import PostFilter
from .forms import PostForm, OtclickForm
from .models import Post, Otvet


class PostsList(ListView): #Общий список обьявлений
    model = Post
    ordering = 'dateCreation'
    template_name = 'posts.html' # не создана страница
    context_object_name = 'posts'
    paginate_by = 10

class MyPosts(ListView): #Список толкьо своих созданных обьявлений
    model = Post
    ordering = 'dateCreation'
    template_name = 'myposts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = Post.objects.filter(user=self.request.user)
        return context

class PostDetail(DetailView): #Полная информация о выбранном обьявлении
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    #queryset = Post.objects.all()

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
def home_page(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['myfile1']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)
        return render(request, 'post_edit.html', {'file_url': file_url })
    return render(request, 'post_edit.html')


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

    # def get_queryset(self): # было, работало
    #     return super().get_queryset()
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Otvets'] = Otvet.objects.filter(Otvet_to__user=self.request.user)
        return context


class OtclickToPost(LoginRequiredMixin, CreateView): #Создание отклика
    model = Otvet
    #form_class = OtclickForm
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
        return reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')}) #

class DeleteOtklick(LoginRequiredMixin, DeleteView):
    model = Otvet
    template_name = 'otklick_delete.html'
    success_url = '/posts/otklicks/'

@login_required
def accept(request, pk):
    Otvet.objects.filter(Otvet_to_id=pk).update(accepted=True)

    instance = Otvet.objects.filter(Otvet_to_id=pk)
    post_author = list(instance.values_list('Otvet_to__user__username', flat=True))
    post_id = list(instance.values_list('Otvet_to__id', flat=True))
    Otvet_user = list(instance.values_list("Otvet_user__username", flat=True))
    email = list(instance.values_list("Otvet_user__email", flat=True))

    send_mail(
        subject=post_author[0],
        message=f"Здравствуйте, {Otvet_user[0]}\n"
                f"Отклик на обьявление {post_id[0]} от пользователя {post_author[0]} был просмотрен и утверждён!",
        from_email='',
        recipient_list=[email[0]])

    return HttpResponseRedirect(f'/otklicks/')

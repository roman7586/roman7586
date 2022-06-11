

# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — newso.html
    template_name = 'newso.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

# Добавляем новое представление для создания постов.
class PostCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

# Для задания 6.2
    #def post(self, request, *args, **kwargs):
    #    post = Post(
    #        author=request.POST['author'],
    #        title=request.POST['title'],
    #        text=request.POST['text'],
    #    )
    #    post.save()
    # #    отправляем письмо
    #    send_mail(subject=f'Вышел новый пост с заголовком {post.title} ',
    #       message=post.text,
    #       from_email='hiromant86@yandex.ru',
    # #       здесь указываете почту, с которой будете отправлять
    #       recipient_list=['hiromant86@mail.ru']  # здесь список получателей.
    #    )
    #    return redirect('news') # надо разобраться

class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post', )


# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('')

#страница авторизованного пользователя и запрос авторства
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'account/indexx.html'

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

class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category.html'
    context_object_name = 'category'


@login_required                                                          # Для задания 6.5
def add_subscribe(request, id):                                                  # Для задания 6.5
    user = request.user                                                  # Для задания 6.5
    category = Category.objects.get(pk=id)                              # Для задания 6.5
    category.subscribers.add(user)                                        # Для задания 6.5
    category.save()                                                       # Для задания 6.5
    return redirect('/news/sub/')                                              # Для задания 6.5
#    CategoryUser = Category.objects.get(name='authors')                    # Для задания 6.5
#    if not request.user.groups.filter(name='authors').exists():          # Для задания 6.5
#        authors_group.user_set.add(user)                                 # Для задания 6.5
#    return redirect('/')                                                 # Для задания 6.5

@receiver(m2m_changed, sender=Post.postCategory.through)
def notify(sender, instance, action, **kwargs):
    mass =[]
    if action == "post_add":
        for i in instance.postCategory.all():
            for j in i.subscribers.all():
                mass.append(j)                                                          #mass.append(j.email) если через получателей в копии

        for user in set(mass):                                                          #убирается, если через получателей в копии
            #send_mail(subject=f'Вышел новый пост с заголовком {instance.title} ',
            #       message=instance.text,
            #       from_email='hiromant86@yandex.ru',
            #       #здесь указываете почту, с которой будете отправлять
            #       recipient_list=[user.email]                                          #recipient_list=set(mass) , если через получателей в копии
            #          )

            #письмо в формате html
            #subject, from_email, to = 'hello', 'hiromant86@yandex.ru', [user.email]
            #text_content = 'This is an important message.'
            #html_content = '<p>This is an <strong>important</strong> message.</p>'
            html_content = render_to_string(
                'news_created.html',
                {
                    'Post': instance,
                    'Category':Category,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Вышел новый пост с заголовком {instance.title}',
                #body=instance.text,
                from_email='hiromant86@yandex.ru',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
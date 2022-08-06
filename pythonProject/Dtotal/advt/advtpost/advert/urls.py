from django.urls import path

from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, home_page

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'), # добавим кэширование на детали товара. Раз в 10 минут (запись в сек) товар будет записываться в кэш для экономии ресурсов.
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('', home_page)
    #path('sub/', CategoryList.as_view(), name='category'),
    #path('subscribe/<int:id>', add_subscribe, name='add_subscribe'),

    #path('indexx/', IndexView.as_view()),
    #path('indexx/upgrade/', upgrade_me, name = 'upgrade')
]
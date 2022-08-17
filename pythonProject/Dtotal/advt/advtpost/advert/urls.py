from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, home_page, OtclickToPost, MyPosts, \
    OtckliksMyPost, DeleteOtklick, accept

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('myposts/', MyPosts.as_view(), name='post_myposts'),

    path('otklicks/', OtckliksMyPost.as_view(), name='otclicks'), #список откликов
    path('<int:pk>/otclick/', OtclickToPost.as_view(), name='otclick'), #написание отклика
    path('otklicks/<int:pk>/delete/', DeleteOtklick.as_view(), name='otklick_delete'),#удаление отклика
    path('otklicks/<int:pk>/accept/', accept), #утверждение отклика

    path('', home_page)


    #path('sub/', CategoryList.as_view(), name='category'),
    #path('subscribe/<int:id>', add_subscribe, name='add_subscribe'),

    #path('indexx/', IndexView.as_view()),
    #path('indexx/upgrade/', upgrade_me, name = 'upgrade')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
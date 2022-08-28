from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete,OtclickToPost, MyPosts, \
    OtckliksMyPost, DeleteOtklick, confirm, newssend

urlpatterns = [

    path('', PostsList.as_view()), # список обьявлений
    path('<int:pk>', PostDetail.as_view(), name='post_detail'), # подробная информация о обьявлении
    path('create/', PostCreate.as_view(), name='post_create'), # Создание обьявления
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'), # Изменение существующего обьявления
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'), # Удаление выбранного обьявления
    path('myposts/', MyPosts.as_view(), name='post_myposts'), # раздел со своими обьявлениями

    path('otklicks/', OtckliksMyPost.as_view(), name='otclicks'), #список откликов
    path('<int:pk>/otclick/', OtclickToPost.as_view(), name='otclick'), #написание отклика
    path('otklicks/<int:pk>/delete/', DeleteOtklick.as_view(), name='otklick_delete'),#удаление отклика
    path('otklicks/<int:id>/confirm/', confirm, name='confirm'), #утверждение отклика

    path('allsend/', newssend), #Сообщение всем(массовая рассылка)

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #для отображения загруженного контента
from django.urls import path

from .views import PostsList, PostDetail, IndexView

urlpatterns = [
   #адреса без авторизации
   path('', PostsList.as_view()), #path('', RedirectView.as_view(url='board'))

   #адреса для авторизованных
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('post/create/', CreateNotice.as_view(), name='board_new'), # создание поста
   path('board/post/<int:pk>/respond/', RespondToPost.as_view(), name='respond'), #отозваться на обьявление
   path('accounts/profile/', MyResponses.as_view(), name='responses'),  # мои отзывы
   path('accounts/profile/post/<int:pk>/', MyResponsesPost.as_view(), name='response_post'),  # Отозвались

   #адреса для автора
   path('index/', IndexView.as_view()),
   path('board/post/<int:pk>/edit/', EditNotice.as_view(), name='board_new'), #редактирование поста
   path('board/post/<int:pk>/delete/', DeletePost.as_view()), #удаление поста
   path('board/response/<int:pk>/accept/', accept), #подтверждение отзыыва
   path('board/response/<int:pk>/delete/', DeleteResponce.as_view()), #удаление отзыыва
]
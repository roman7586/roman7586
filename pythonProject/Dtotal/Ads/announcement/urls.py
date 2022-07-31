from django.urls import path

from .views import PostsList, PostDetail, IndexView

urlpatterns = [
   #адреса без авторизации
   path('', PostsList.as_view()),

   #адреса для авторизованных
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),

   #адреса для автора
   path('index/', IndexView.as_view())
]
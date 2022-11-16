from django.urls import path

from . import views
from .views import room_create
urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
    path('<slug:slug>/delete/', views.room_delete, name='room_delete'),
    path('<slug:slug>/edit/', views.room_edit, name='room_edit'),
    path('create/', room_create, name='room_create'),
]

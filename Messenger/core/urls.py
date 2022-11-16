from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.frontpage, name="frontpage"),
    path('signup/', views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', views.show_profile, name='profile'),
    path('users/', views.users, name='users'),
    path('chat/<int:pk>/', views.direct_messages, name='direct_message')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
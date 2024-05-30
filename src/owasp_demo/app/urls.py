from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('search_users/', views.search_users, name='search_users'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
]

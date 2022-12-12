from django.urls import path
from .views import register, profile
from django.contrib.auth import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('profile/', profile, name='profile')
]

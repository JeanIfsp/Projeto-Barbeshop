from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_confirm/<str:tokenstr>/<str:tokendate>/', views.password_reset_confirm, name='password_reset_confirm'),
]

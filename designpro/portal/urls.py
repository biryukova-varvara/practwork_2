from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.register, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
]

urlpatterns += [
    path('request/create/', views.create_request, name='cr_request'),
    path('request/<int:pk>/delete/', views.delete_request, name='delete_request'),
    path('manage/requests/', views.admin_requests, name='admin_requests'),
    path('manage/request/<int:pk>/change-status/', views.change_status, name='change_status'),
]
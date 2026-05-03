from django.http import JsonResponse
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import search_view

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),

    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('user/<str:username>/', views.user_public_profile, name='user_public_profile'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/delete/<int:pk>/', views.delete_notification, name='delete_notification'),
    path('notifications/clear-all/', views.clear_all_notifications, name='clear_all_notifications'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='reset_password'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('contact/', views.contact, name='contact'),
    path('get-notifications-count/', lambda r: JsonResponse({'count': 0}), name='get_notifications_count'),

    path('search/', search_view, name='search'),
]
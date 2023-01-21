from django.urls import path
# from  .import views as user_views

from .import views
# from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('register/', user_views.register, name='register'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user_app/logout.html'), name='logout'),
    path('profile', views.profile, name='profile'),
    path('profile/update', views.profileupdate, name='profile-update'),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='user_app/password-change.html'),name='password-change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user_app/password-change-done.html'), name='password_change_done'),




    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='user_app/password_reset.html'),name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user_app/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user_app/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user_app/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    ]
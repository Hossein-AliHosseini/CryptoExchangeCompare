from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('activate/<slug:eid>/<slug:token>',
         activate, name='activate'),
    # path('change_password/', change_password_view,
    #      name="change_password"),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name="profile"),
    path("password_reset/", password_reset_request, name="password_reset"),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),
]

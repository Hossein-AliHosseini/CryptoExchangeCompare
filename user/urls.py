from django.urls import path

from .views import *

urlpatterns = [
    path('user/signup/', signup_view, name="signup"),
    path('user/login/', login_view, name="login"),
    path('user/activate/<slug:eid>/<slug:token>',
         activate, name='activate'),
    path('user/change_password/', change_password_view,
         name="change_password"),
    path('user/logout/', logout_view, name='logout'),
    path('user/profile/', profile_view, name="profile"),
]

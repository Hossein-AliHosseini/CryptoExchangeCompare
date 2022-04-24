from django.urls import path

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
    path("password_reset/", password_reset_request, name="password_reset")
]

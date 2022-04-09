from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('user/signup/', signup_view, name="signup"),
    path('user/login/', login_view, name="login"),
    path('user/home/', home_view, name="home"),
    path('user/activate/<slug:eid>/<slug:token>',
         activate, name='activate'),
    path('user/change_password/', change_password_view,
         name="change_password"),
    path('user/logout/', logout_view, name='logout'),
    path('user/profile/', profile_view, name="profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

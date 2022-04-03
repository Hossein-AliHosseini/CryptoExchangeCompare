from django.urls import path

from .views import *

urlpatterns = [
    path('login', view=LoginAPIView.as_view(), name='login'),
    path('is-active', view=IsActivatedAPIView.as_view(), name='is_active'),
    path('signup', view=SignUpAPIView.as_view(), name='signup'),
    path('activate/<slug:eid>/<slug:token>', view=ActivateAPIView.as_view(),
         name='activate'),
    path('logout', view=LogoutAPIView.as_view(), name='logout'),
    path('resend-activation-link', view=ResendActivationEmailAPIView.as_view(),
         name='resend'),
    path('person', view=PersonAPIView.as_view(), name='person'),
    path('password/change', ChangePasswordAPIView.as_view()),
    path('password/reset', view=ResetPasswordAPIView.as_view(),
         name='reset password'),
    path('password/reset/confirm', view=ResetPasswordConfirmAPIView.as_view(),
         name='confirm password'),
]

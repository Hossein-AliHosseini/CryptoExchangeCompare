from django.urls import path

from .views import dt_report, ht_report, cumulative_report,\
    UserAutocomplete, email_autocomplete, username_autocomplete,\
        check_status
from user.models import User

urlpatterns = [
    path('dt_report/', dt_report, name='report_dt'),
    path('ht_report', ht_report, name='report_ht'),
    path('cumulative_report/', cumulative_report, name='report_cumulative'),
    path('user-autocomplete/',
         UserAutocomplete.as_view(),
         name='user-autocomplete'),
    path('email-autocomplete/', email_autocomplete, name='email-autocomplete'),
    path('username-autocomplete/', username_autocomplete, name='username-autocomplete'),
    path('check_status/', check_status, name='check_status')
]

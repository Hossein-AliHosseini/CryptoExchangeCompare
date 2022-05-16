from django.urls import path

from .views import dt_report, ht_report

urlpatterns = [
    path('dt_report/', dt_report, name='report_dt'),
    path('ht_report', ht_report, name='report_ht')
]

from django.urls import path

from .views import transaction_view, exchange_account_view

urlpatterns = [
    path('transaction/', transaction_view, name='transaction'),
    path('account/', exchange_account_view, name='account'),
]

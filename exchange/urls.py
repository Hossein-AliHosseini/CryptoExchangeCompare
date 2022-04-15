from django.urls import path

from .views import transaction_view, exchange_account_view, profitandloss_view, orderbooks_view

urlpatterns = [
    path('transaction/', transaction_view, name='transaction'),
    path('account/', exchange_account_view, name='account'),
    path('profitloss/', profitandloss_view, name='pandl'),
    path('orderbooks/', orderbooks_view, name='orderbooks')
]

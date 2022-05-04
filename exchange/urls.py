from django.urls import path

from .views import transaction_view, exchange_account_view,\
    profitandloss_view, orderbooks_view, account_edit_view,\
    trade_view, choice_details, withdraw_view, withdraw_confirm_view

urlpatterns = [
    path('transaction/', transaction_view, name='transaction'),
    path('account/', exchange_account_view, name='account'),
    path('profitloss/', profitandloss_view, name='pandl'),
    path('orderbooks/', orderbooks_view, name='orderbooks'),
    path('edit-account/<int:pk>/', account_edit_view, name='edit_account'),
    path('trade/<str:currency>/<str:market>/', trade_view, name='trade'),
    path('choice/', choice_details, name='choices'),
    path('withdraw/', withdraw_view, name='withdraw'),
    path('withdraw-confirm/<str:withdraw_id>/', withdraw_confirm_view, name='withdraw-confirm'),
]

import django_filters

from exchange.models import Transaction, Account


class TransactionFilter(django_filters.FilterSet):
    created__gt = django_filters.NumberFilter(field_name='Start Date',
                                              lookup_expr='created__gt')
    created__lt = django_filters.NumberFilter(field_name='End Date',
                                              lookup_expr='created__lt')

    class Meta:
        model = Transaction
        exclude = ('id', 'dual_transaction', 'completion_date',
                   'transaction_fee', 'created', 'modified', 'stop_limit',
                   'transaction_id', 'size', 'price')


class AccountFilter(django_filters.FilterSet):
    created__gt = django_filters.DateFilter(field_name='Start Date',
                                            lookup_expr='created__gt')
    created__lt = django_filters.DateFilter(field_name='End Date',
                                            lookup_expr='created__lt')

    class Meta:
        model = Account
        exclude = ('id', 'token', 'wallet_address',
                   'exchange_password', 'created', 'modified')

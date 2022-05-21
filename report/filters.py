from django import forms

import django_filters

from user.models import User
from exchange.models import Transaction, Account


class TransactionFilter(django_filters.FilterSet):
    created__gt = django_filters.DateFilter(field_name='created',
                                            lookup_expr='gte',
                                            label='Creation Date Start',
                                            widget=forms.DateInput(
                                                     attrs={'id': 'datepicker',
                                                            'type': 'date'}
                                                    ))
    created__lt = django_filters.DateFilter(field_name='created',
                                            lookup_expr='lte',
                                            label='Creation Date End',
                                            widget=forms.DateInput(
                                                  attrs={'id': 'datepicker',
                                                         'type': 'date'}
                                               ))

    class Meta:
        model = Transaction
        exclude = ('id', 'dual_transaction', 'completion_date',
                   'transaction_fee', 'created', 'modified', 'stop_limit',
                   'transaction_id', 'size', 'price')


class AccountFilter(django_filters.FilterSet):
    created__gt = django_filters.DateFilter(field_name='created',
                                            lookup_expr='gt',
                                            label='Creation Date Start',
                                            widget=forms.DateInput(
                                                  attrs={'id': 'datepicker',
                                                         'type': 'date'}
                                                       ))
    created__lt = django_filters.DateFilter(field_name='created',
                                            lookup_expr='lt',
                                            label='Creation Date End',
                                            widget=forms.DateInput(
                                                    attrs={'id': 'datepicker',
                                                           'type': 'date'}
                                                 ))

    class Meta:
        model = Account
        exclude = ('id', 'token', 'wallet_address',
                   'exchange_password', 'created', 'modified')


class UserFilter(django_filters.FilterSet):
    date_joined__date__gte = django_filters.DateFilter(field_name='date_joined',
                                                       lookup_expr='date__gte',
                                                       label='Joining Date Start',
                                                       widget=forms.DateInput(
                                                          attrs={'id': 'datepicker',
                                                                 'type': 'date'}
                                                       ))
    date_joined__date__lte = django_filters.DateFilter(field_name='date_joined',
                                                       lookup_expr='date__lte',
                                                       label='Joining Date End',
                                                       widget=forms.DateInput(
                                                          attrs={'id': 'datepicker',
                                                                 'type': 'date'}
                                                       ))

    class Meta:
        model = User
        exclude = ('id', 'last_login', 'is_staff',
                   'password', 'last_name', 'first_name',
                   'user_permissions', 'groups', 'date_joined')

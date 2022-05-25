from secrets import choice
from django import forms

import django_filters
from dal import autocomplete, widgets

from user.models import User
from exchange.models import Transaction, Account, ExchangeChoice, Crypto, TransactionType


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
    username = django_filters.ModelChoiceFilter(field_name='username',
                                                lookup_expr='icontains',
                                                label="Username",
                                                queryset=User.objects.all())
    email = django_filters.CharFilter(field_name='email',
                                      lookup_expr='icontains',
                                      label='Email',)
                                    #   widget=autocomplete.Select2(url='user-autocomplete'))
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
    account__owner__username__icontains = django_filters.CharFilter(field_name='account',
                                                                    lookup_expr='owner__username__icontains',
                                                                    label='Account Owner')
    account__exchange = django_filters.ChoiceFilter(field_name='account',
                                                    lookup_expr='exchange',
                                                    label="Account Exchange",
                                                    choices=ExchangeChoice.TYPES,)
    transaction__crypto = django_filters.ChoiceFilter(field_name='transaction',
                                                      lookup_expr='crypto',
                                                      label='Transaction Crypto',
                                                      choices=Crypto.TYPES,)
    transaction__exchange = django_filters.ChoiceFilter(field_name='transaction',
                                                        lookup_expr='exchange',
                                                        label="Transaction Exchange",
                                                        choices=ExchangeChoice.TYPES,)
    transaction__type = django_filters.ChoiceFilter(field_name='transaction',
                                                   lookup_expr='type',
                                                   label='Transaction Type',
                                                   choices=TransactionType.TYPES,)
    transaction__created__date__gte_ = django_filters.DateFilter(field_name='transaction',
                                                                 lookup_expr='created__date__gte',
                                                                 label='Transaction Creation Date Start',
                                                                 widget=forms.DateInput(
                                                                    attrs={'id': 'datepicker',
                                                                           'type': 'date'}
                                                                 ))
    transaction__created__date__lte_ = django_filters.DateFilter(field_name='transaction',
                                                                 lookup_expr='created__date__lte',
                                                                 label='Transaction Creation Date End',
                                                                 widget=forms.DateInput(
                                                                    attrs={'id': 'datepicker',
                                                                           'type': 'date'}
                                                                 ))

    class Meta:
        model = User
        exclude = ('id', 'last_login', 'is_staff',
                   'password', 'last_name', 'first_name',
                   'user_permissions', 'groups', 'date_joined')
        # widgets = {
        #     'email': autocomplete.ModelSelect2(url='user-autocomplete')
        # }
